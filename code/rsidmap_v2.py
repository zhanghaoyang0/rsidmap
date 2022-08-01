import os
import gzip
import time
import argparse
import numpy as np

start = time.time()
### flags parser
parser = argparse.ArgumentParser(description='rsidmap_v2')
parser.add_argument('--build', type=str, default='hg19')
parser.add_argument('--exact_map', type=bool, default=False)
parser.add_argument('--chr_col', type=str, default='CHR')
parser.add_argument('--pos_col', type=str, default='POS')
parser.add_argument('--ref_col', type=str, default='REF')
parser.add_argument('--alt_col', type=str, default='ALT')
parser.add_argument('--file_gwas', type=str, default='./example/df_hg19.txt')
parser.add_argument('--file_out', type=str, default='./example/df_hg19_withrsid.txt')
args = parser.parse_args()

build = args.build
chr_col = args.chr_col; pos_col = args.pos_col; ref_col = args.ref_col; alt_col = args.alt_col
file_gwas = args.file_gwas; file_out = args.file_out
exact_map = args.exact_map

print('Setting:')
print('build: '+ build)
print('chr_col: '+ chr_col); print('pos_col: '+ pos_col); print('ref_col: '+ ref_col); print('alt_col: '+ alt_col)
print('file_gwas: '+ file_gwas); print('file_out: '+ file_out)
print('exact_map: '+ str(exact_map))

### ncid dict and functions
def find_rsid(items, chr, pos, ref, alt, exact_map):
    # indel must exact_map (i.e., C>CT != CT>C)
    exact_map1 = True if (len(alt)>1)|(len(ref)>1) else exact_map 
    snp = f'{chr}:{pos}:{ref}:{alt}' # pseudo snp
    if len(items)==0: return(snp)
    # break multi allele (e.g., A,G>T to A>G and C>T)
    items1 = [] # alt combination
    for item in items:
        items1 += [[item[0], x, y] for x in item[1].split(',') for y in item[2].split(',')]
    flags = [[x[1], x[2]]==[ref, alt] if exact_map1 else {x[1], x[2]}=={ref, alt} for x in items1]
    if sum(flags)>0: snp = np.array(items1)[flags][0][0] # greedy map, use first
    return(snp)


# these two dicts are reversed from that in rsidmap
d19 = {'NC_000001.10': '1', 'NC_000002.11': '2', 'NC_000003.11': '3', 'NC_000004.11': '4', 'NC_000005.9': '5', 'NC_000006.11': '6', 
    'NC_000007.13': '7', 'NC_000008.10': '8', 'NC_000009.11': '9', 'NC_000010.10': '10', 'NC_000011.9': '11', 'NC_000012.11': '12', 
    'NC_000013.10': '13', 'NC_000014.8': '14', 'NC_000015.9': '15', 'NC_000016.9': '16', 'NC_000017.10': '17', 'NC_000018.9': '18', 
    'NC_000019.9': '19', 'NC_000020.10': '20', 'NC_000021.8': '21', 'NC_000022.10': '22', 'NC_000023.10': 'X', 'NC_000024.9': 'Y', 'NC_012920.1': 'M'}
d38 = {'NC_000001.11': '1', 'NC_000002.12': '2', 'NC_000003.12': '3', 'NC_000004.12': '4', 'NC_000005.10': '5', 'NC_000006.12': 
    '6', 'NC_000007.14': '7', 'NC_000008.11': '8', 'NC_000009.12': '9', 'NC_000010.11': '10', 'NC_000011.10': '11', 'NC_000012.12': 
    '12', 'NC_000013.11': '13', 'NC_000014.9': '14', 'NC_000015.10': '15', 'NC_000016.10': '16', 'NC_000017.11': '17', 'NC_000018.10': '18', 
    'NC_000019.10': '19', 'NC_000020.11': '20', 'NC_000021.9': '21', 'NC_000022.11': '22', 'NC_000023.11': 'X', 'NC_000024.10': 'Y', 'NC_012920.1': 'M'}

ncid2chr = {'hg19': d19, 'hg38': d38}
file_dbsnp = {'hg19': './dbsnp_v155/GCF_000001405.25.gz', 'hg38': './dbsnp_v155/GCF_000001405.39.gz'}


# default setting, for test
build = 'hg19'
chr_col = 'CHR'
pos_col = 'POS'
ref_col = 'A2'
alt_col = 'A1'
file_gwas = './example/df_hg19.txt'
file_out = './example/df_hg19_withrsid.txt'
exact_map = False

### make dbsnp dict
print (f'making dnsnp dict ...')
time1 = time.time()
# dnsnp_key
line = open(file_gwas).readline()
idx = [line.split().index(x) for x in [chr_col, pos_col, ref_col, alt_col]] # idx for chr, pos, ref, alt
with open(file_gwas) as f:
    dnsnp_key = {tuple([i[x] for x in idx[:2]]) for i in (line.split() for line in f)}

# dnsnp_key value
dbsnp = dict()
with gzip.open(file_dbsnp[build], 'rt') as f: 
    for line in f:
        if "#" in line: continue
        items = line.split()
        token = tuple([ncid2chr[build][items[0]], items[1]])
        if token in dnsnp_key:
            if token in dbsnp: dbsnp[token] = dbsnp[token] + [items[2:5]]
            else: dbsnp[token] = [items[2:5]]
            print(len(dbsnp))

time2 = time.time()
print (f'spend {time.strftime("%M min %S sec", time.gmtime(time2-time1))}')

### annotate
print (f'finding dnsnp dict ...')
res = open(file_out, 'w')
nrow = len(list(open(file_gwas)))
i = 1; n_map = 0

open_f = gzip.open(file_gwas, 'rt') if '.gz' in file_gwas else open(file_gwas)

with open(file_gwas) as f:
    for line in f:
        if i % round(nrow/50)==0: print(f'processed {i}/{nrow} snp ({round(100*i/nrow, 1)}%)')
        if i == 1: # header
            out = line.replace('\n', '\tSNP\n')
        else:
            chr, pos, ref, alt = [line.split()[x] for x in idx]
            if (chr, pos) in dbsnp: items = dbsnp[(chr, pos)]
            else: items = []
            snp = find_rsid(items, chr, pos, ref, alt, exact_map)
            if 'rs' in snp: n_map += 1
            out = line.replace('\n', '\t'+snp+'\n')
        i += 1
        _ = res.write(out) # use a variable to aviod printing

res.close()

time3 = time.time()
print(f'N. rsid maped: {n_map}, done!')
print (f'spend {time.strftime("%M min %S sec", time.gmtime(time3-time1))}')