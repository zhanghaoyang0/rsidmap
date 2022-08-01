
# About rsidmap
`rsidmap` is a tool for to find rsid with genome postion in a GWAS summary.

# Why rsidmap
- Full:  
`rsidmap` uses latest dbsnp release (build 155, available at 20210616, >20G for a build) to perform quick search with 
*tabix*.

- Convenient:  
`rsidmap` uses a (tab separated) gwas summary as input and provides output with a new rsid field. 

- Fleasible:  
`rsidmap` provides a flag `--exact_map` to chose if you want exact match or not, default is False.  
Example:  
exact_map = True: only 1:10055:T:C would be mapped to rs892501864.  
exact_map = False:, both 1:10055:T:C and 1:10055:C:T would be mapped to rs892501864.   
Tools like ANNOVAR provides only [excat map](https://annovar.openbioinformatics.org/en/latest/articles/dbSNP/).  
A fleasible map (exact_map = False) is useful because in some analysis when two alleles can be reordered by taking opposite GWAS effect.  
Note that indel would be exact map. 
Example:  
1:10055:C:CT would be mapped to rs1639543798  
1:10055:CT:C would be mapped to rs1639543820

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

Download latest_release dbsnp with `wget`:
```
wget -c https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.25.gz -P dbsnp_v155/
wget -c https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.39.gz -P dbsnp_v155/
wget -c https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.25.gz.tbi -P dbsnp_v155/
wget -c https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.39.gz.tbi -P dbsnp_v155/
```

Once the above has completed, you can try to add rsid field by specifying: 
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
--file_out ./example/df_hg19_withrsid.txt

python ./code/rsidmap.py \
--build hg38 \
--chr_col chrom --pos_col pos --ref_col ref --alt_col alt \
--file_gwas ./example/df_hg38.txt \
--file_out ./example/df_hg38_withrsid.txt
```

gzip (file_gwas end with '.gz') input can be recongized: 
```
python ./code/rsidmap.py \
--build hg19 \
--chr_col CHR --pos_col POS --ref_col A2 --alt_col A1 \
--file_gwas ./example/df_hg19.txt.gz \
--file_out ./example/df_hg19_withrsid.txt
```

The input file is like:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P
1   10054   C   CT  0.2313  0.002   0.23    0.3121
1   10054   CT  C   0.1213  0.042   0.12    0.0031
1   10054   T   A   0.165   0.011    0.63   0.0259
1   10054   T   C   0.151   0.023    0.02   0.0121
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035
12      104289454       T       C       0.534   0.0085  0.0088  0.3322
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256
4       163471758       T       C       0.612   0.0119  0.0094  0.2057
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
file_out: ./example/df_hg19_withrsid.txt
exact_map: False
processed 10/501 snp (2.0%)
processed 20/501 snp (4.0%)
processed 30/501 snp (6.0%)
processed 40/501 snp (8.0%)
processed 50/501 snp (10.0%)
...
```

If `rsidmap` finnised, you will see number of snp map to dbsnp:
```
processed 480/501 snp (95.8%)
processed 490/501 snp (97.8%)
processed 500/501 snp (99.8%)
N. rsid maped: 500, done!
spend 27.02 sec
```

The output file is like:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P       SNP
1   10054   C   CT  0.2313  0.002   0.23    0.3121      rs1639543820
1   10054   CT  C   0.1213  0.042   0.12    0.0031      rs1639543798
1   10054   T   A   0.165   0.011    0.63   0.0259      rs892501864
1   10054   T   C   0.151   0.023    0.02   0.0121      rs892501864
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101  rs13387171
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397 rs13175391
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035 rs58796836
12      104289454       T       C       0.534   0.0085  0.0088  0.3322  rs9888379
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256 rs182678857
4       163471758       T       C       0.612   0.0119  0.0094  0.2057  rs10019229
```
Note that pseudo ids (CHR:POS:REF:ALT) would be added if not matched.  
You can check with `grep -v "rs" ./example/df_hg38_withrsid.txt`
```
chrom   pos     ref     alt     SNP
3       133449405       C       CTTTGTT 3:133449405:C:CTTTGTT
4       38201325        TG      T       4:38201325:TG:T
7       101169297       AAC     A       7:101169297:AAC:A
22      19836880        T       TA      22:19836880:T:TA
7       105265861       A       AT      7:105265861:A:AT
4       83064334        TA      T       4:83064334:TA:T
12      132410689       G       A       12:132410689:G:A
```

# Acknowledgement
Thank Dr. Guowang Lin for his inspiration.

# Feedback and comments
Feel free to add a issue or contact me via zhanghaoyang0@hotmail.com