
# About rsidmap
`rsidmap` is a tool for to find rsid with genome postion in a GWAS summary.

# Why rsidmap
- Full:  
`rsidmap` uses latest dbsnp release (build 155, available at 20210616, >20G for a build) to perform quick search.

- Convenient:  
`rsidmap` uses a (tab separated) gwas summary as input and provides output with a new rsid field. 

- Fleasible:  
`rsidmap` provides a flag `--exact_map` to chose if you want exact match or not, default is False.  
Tools like ANNOVAR provides only [excat map](https://annovar.openbioinformatics.org/en/latest/articles/dbSNP/).
A fleasible map (exact_map = False) is useful because in some analysis, two alleles can be reordered by taking opposite GWAS effect.
Note that indel would be exact map (even you have set exact_map = False).
Example:  
```
# exact_map
exact_map = True: only 1:10055:T:C would be mapped to rs892501864.  
exact_map = False:, both 1:10055:T:C and 1:10055:C:T would be mapped to rs892501864.  
# indel 
1:10055:C:CT would be mapped to rs1639543798  
1:10055:CT:C would be mapped to rs1639543820
```

# Requirements
- `Linux` with `wget` and `tabix`
- `Python3` (3.9.6) with `numpy` (1.23.1), `argparse`, `gzip`, `os`, `time`  
  
Versions I used are in bracket

# Getting Started
Clone this repository via the commands:
```  
git clone https://github.com/zhanghaoyang0/rsidmap.git
cd rsidmap
```

Download latest_release dbsnp with `wget`, and verify your dbsnp with `md5sum`:
```
url="https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/"
dbsnp_hg19="GCF_000001405.25"
dbsnp_hg38="GCF_000001405.40"

# for hg 19
wget -c ${url}${dbsnp_hg19}.gz -P dbsnp/
wget -c ${url}${dbsnp_hg19}.gz.md5 -P dbsnp/
wget -c ${url}${dbsnp_hg19}.gz.tbi -P dbsnp/
wget -c ${url}${dbsnp_hg19}.gz.tbi.md5 -P dbsnp/

# for hg38
wget -c ${url}${dbsnp_hg38}.gz -P dbsnp/
wget -c ${url}${dbsnp_hg38}.gz.md5 -P dbsnp/
wget -c ${url}${dbsnp_hg38}.gz.tbi -P dbsnp/
wget -c ${url}${dbsnp_hg38}.gz.tbi.md5 -P dbsnp/

# check md5sum
cd dbsnp
md5sum -c ${dbsnp_hg19}.gz.md5
md5sum -c ${dbsnp_hg19}.gz.tbi.md5
md5sum -c ${dbsnp_hg38}.gz.md5
md5sum -c ${dbsnp_hg38}.gz.tbi.md5
cd ../

## note
# If you can not download with prevous link, add an issue.  
# The possible reason is dbsnp is updated and I need to update my code.
```

If your dbsnp is correct, you will see:
```
GCF_000001405.25.gz: OK
GCF_000001405.25.gz.tbi: OK
GCF_000001405.40.gz: OK
GCF_000001405.40.gz.tbi: OK 
```

Then, you can try to add rsid field by specifying: 
`--build` hg19 or hg38  
`--chr_col` field name of CHR, default is CHR   
`--pos_col` field name of POS, default is POS  
`--ref_col` field name of REF, default is REF  
`--alt_col` field name of ALT, default is ALT  
`--exact_map` excat map or not, default is False  
`--file_gwas` tab[\t] separated input file, gzip (file_gwas end with '.gz') input can also be recongized  
`--file_out` output file  

Two examples (hg19 and hg38):
```
python ./code/rsidmap.py \
--build hg19 \
--chr_col CHR --pos_col POS --ref_col A2 --alt_col A1 \
--file_gwas ./example/df_hg19.txt \
--file_out ./example/df_hg19_rsidmap.txt

python ./code/rsidmap.py \
--build hg38 \
--chr_col chrom --pos_col pos --ref_col ref --alt_col alt \
--file_gwas ./example/df_hg38.txt \
--file_out ./example/df_hg38_rsidmap.txt
```

gzip (file_gwas end with '.gz') input can be recongized: 
```
python ./code/rsidmap.py \
--build hg19 \
--chr_col CHR --pos_col POS --ref_col A2 --alt_col A1 \
--file_gwas ./example/df_hg19.txt.gz \
--file_out ./example/df_hg19_rsidmap.txt
```

The input file is like:
```
CHR	POS	A1	A2	FRQ	BETA	SE	P
X   393109  T   C   0.512	0.131	0.25	0.029
1	10054	C	CT	0.2313	0.002	0.23	0.3121
1	10054	CT	C	0.1213	0.042	0.12	0.0031
Y   10002   T   A   0.614	0.28	0.095	0.421
1	10054	T	A	0.165	0.011	0.63	0.0259
1	10054	T	C	0.151	0.023	0.02	0.0121
2	48543917	A	G	0.4673	0.0045	0.0088	0.6101
5	87461867	A	G	0.7151	0.0166	0.0096	0.08397
14	98165673	T	C	0.1222	-0.0325	0.014	0.02035
```

If `rsidmap` is running, you will see:
```
Setting:
build: hg19
chr_col: CHR
pos_col: POS
ref_col: A2
alt_col: A1
file_gwas: ./example/df_hg19.txt
file_out: ./example/df_hg19_rsidmap.txt
exact_map: False
processed 24/500 snp (4.8%)
processed 49/500 snp (9.8%)
... 
processed 474/500 snp (94.8%)
processed 499/500 snp (99.8%)
N. rsid maped: 498, done!
spend 27.02 sec
```

The output file is like:
```
CHR	POS	A1	A2	FRQ	BETA	SE	P	SNP
X   393109  T   C   0.512	0.131	0.25	0.029	rs1603207647
1	10054	C	CT	0.2313	0.002	0.23	0.3121	rs1639543820
1	10054	CT	C	0.1213	0.042	0.12	0.0031	rs1639543798
Y   10002   T   A   0.614	0.28	0.095	0.421	rs1226858834
1	10054	T	A	0.165	0.011	0.63	0.0259	1:10054:A:T
1	10054	T	C	0.151	0.023	0.02	0.0121	1:10054:C:T
2	48543917	A	G	0.4673	0.0045	0.0088	0.6101	rs13387171
5	87461867	A	G	0.7151	0.0166	0.0096	0.08397	rs13175391
14	98165673	T	C	0.1222	-0.0325	0.014	0.02035	rs58796836
```
Note that pseudo ids (CHR:POS:REF:ALT) would be added if not matched.  
You can check with `grep -v "rs" ./example/df_hg19_rsidmap.txt`
```
CHR     POS     A1      A2      FRQ     BETA    SE      P       SNP
1       10054   T       A       0.165   0.011   0.63    0.0259  1:10054:A:T
1       10054   T       C       0.151   0.023   0.02    0.0121  1:10054:C:T
```

# For large dataset
- If your gwas is small, use `rsidmap.py` is enough. It process ~20 snp a sec.  
- If your gwas is large (e.g., > 1M snp), use `rsidmap_v2.py`.  
  It takes ~30min to build a python dictionary and then map to your gwas quickly.
  
Examples:
```
python ./code/rsidmap_v2.py \
--build hg19 \
--chr_col chr --pos_col pos --ref_col a2 --alt_col a1 \
--file_gwas ./example/largedf_hg19.txt.gz \
--file_out ./example/largedf_hg19_rsidmapv2.txt

python ./code/rsidmap_v2.py \
--build hg19 \
--chr_col CHR --pos_col POS --ref_col A2 --alt_col A1 \
--file_gwas ./example/df_hg19.txt.gz \
--file_out ./example/df_hg19_rsidmapv2.txt
```
If `rsidmap_v2` is running, you will see:
```
Setting:
build: hg19
chr_col: chr
pos_col: pos
ref_col: a2
alt_col: a1
file_gwas: ./example/largedf_hg19.txt.gz
file_out: ./example/largedf_hg19_rsidmapv2.txt
exact_map: False
making dnsnp dict ...
1000000 unique and valid snp.
processed 50000/1000000 snp (5.0%)
processed 100000/1000000 snp (10.0%)
...
processed 950000/1000000 snp (95.0%)
done!
finding dnsnp dict ...
done! N. rsid mapped: 999593
spend 40 min 15 sec
```
# Acknowledgement
Many thanks to Dr. Guowang Lin for his inspiration and help.

# Feedback and comments
Add an issue or contact me via zhanghaoyang0@hotmail.com
