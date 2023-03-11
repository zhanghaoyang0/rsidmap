import os
import gzip
import time
import argparse
import numpy as np

start = time.time()
### flags parser
parser = argparse.ArgumentParser(description='rsidmap')
parser.add_argument('--build', type=str, default='hg19')
parser.add_argument('--exact_map', type=bool, default=False)
parser.add_argument('--chr_col', type=str, default='CHR')
parser.add_argument('--pos_col', type=str, default='POS')
parser.add_argument('--ref_col', type=str, default='REF')
parser.add_argument('--alt_col', type=str, default='ALT')
parser.add_argument('--file_gwas', type=str, default='./example/df_hg19.txt')
parser.add_argument('--file_out', type=str, default='./example/df_hg19_rsidmap.txt')
args = parser.parse_args()

build = args.build
chr_col = args.chr_col; pos_col = args.pos_col; ref_col = args.ref_col; alt_col = args.alt_col
file_gwas = args.file_gwas; file_out = args.file_out
exact_map = args.exact_map

# # default setting, for test
# build = 'hg19'
# chr_col = 'CHR'
# pos_col = 'POS'
# ref_col = 'A2'
# alt_col = 'A1'
# file_gwas = './example/df_hg19.txt.gz'
# file_out = './example/df_hg19_rsidmap.txt'
# exact_map = False

print('Setting:')
print('build: '+ build)
print('chr_col: '+ chr_col); print('pos_col: '+ pos_col); print('ref_col: '+ ref_col); print('alt_col: '+ alt_col)
print('file_gwas: '+ file_gwas); print('file_out: '+ file_out)
print('exact_map: '+ str(exact_map))

### dicts and functions
def find_rsid(items, chr, pos, ref, alt, exact_map):
    # indel must exact_map (i.e., C>CT != CT>C)
    exact_map1 = True if (len(alt)>1)|(len(ref)>1) else exact_map 
    snp = f'{chr}:{pos}:{ref}:{alt}' # pseudo snp
    if len(items)==0: return(snp)
    else: 
        items = [x.split()[2:5] for x in items] # select useful fields
        # break multi allele (e.g., A,G>T to A>G and C>T)
        items1 = [] # alt combination
        for item in items:
            items1 += [[item[0], x, y] for x in item[1].split(',') for y in item[2].split(',')]
        flags = [[x[1], x[2]]==[ref, alt] if exact_map1 else {x[1], x[2]}=={ref, alt} for x in items1]
        if sum(flags)>0: snp = np.array(items1)[flags][0][0] # greedy map, use first
        return(snp)

def openfile(filename):
    if filename.endswith('.gz'): return gzip.open(filename, 'rt') 
    else: return open(filename)

d19 = {"1": "NC_000001.10", "2": "NC_000002.11", "3": "NC_000003.11", "4": "NC_000004.11","5": "NC_000005.9", 
    "6": "NC_000006.11", "7": "NC_000007.13", "8": "NC_000008.10","9": "NC_000009.11", "10": "NC_000010.10", 
    "11": "NC_000011.9", "12": "NC_000012.11","13": "NC_000013.10", "14": "NC_000014.8", "15": "NC_000015.9",
    "16": "NC_000016.9","17": "NC_000017.10", "18": "NC_000018.9", "19": "NC_000019.9", "20": "NC_000020.10",
    "21": "NC_000021.8", "22": "NC_000022.10", "X": "NC_000023.10", "Y": "NC_000024.9", 'M': "NC_012920.1"}
d38 = {"1": "NC_000001.11", "2": "NC_000002.12", "3": "NC_000003.12", "4": "NC_000004.12", "5": "NC_000005.10", 
    "6": "NC_000006.12", "7": "NC_000007.14", "8": "NC_000008.11", "9": "NC_000009.12", "10": "NC_000010.11", 
    "11": "NC_000011.10", "12": "NC_000012.12", "13": "NC_000013.11", "14": "NC_000014.9", "15": "NC_000015.10", 
    "16": "NC_000016.10", "17": "NC_000017.11", "18": "NC_000018.10", "19": "NC_000019.10", "20": "NC_000020.11",
    "21": "NC_000021.9", "22": "NC_000022.11", "X": "NC_000023.11", "Y": "NC_000024.10", "M": "NC_012920.1"}
chr2ncid = {'hg19': d19, 'hg38': d38}
file_dbsnp = {'hg19': './dbsnp/GCF_000001405.25.gz', 'hg38': './dbsnp/GCF_000001405.40.gz'}

cols = [chr_col, pos_col, ref_col, alt_col]
res = open(file_out, 'w')
nsnp = len(list(openfile(file_gwas)))-1; i = 1; n_map = 0

with openfile(file_gwas) as f:
    for line in f:
        if i % round(nsnp/20)==0: print(f'processed {i-1}/{nsnp} snp ({round(100*(i-1)/nsnp, 1)}%)')
        if i == 1: # header row
            idx = [line.split().index(x) for x in cols] # idx for chr, pos, a1, a2
            out = line.replace('\n', '\tSNP\n')
        else:
            chr, pos, ref, alt = [line.split()[x] for x in idx]
            ncid = chr2ncid[build][str(chr)] # chr id in dbsnp
            items = os.popen(f'tabix {file_dbsnp[build]} {ncid}:{pos}-{int(pos)}').readlines()
            snp = find_rsid(items, chr, pos, ref, alt, exact_map)
            if 'rs' in snp: n_map += 1
            out = line.replace('\n', '\t'+snp+'\n')
        _ = res.write(out) # use a variable to aviod printing
        i += 1

res.close()

end = time.time()
print(f'done! N. rsid mapped: {n_map}')
print (f'spend {round(end-start, 2)} sec')