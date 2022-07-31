
# About rsidmap
`rsidmap` is a tool for to find rsid with genome postion in a GWAS summary.

# Why rsidmap
- Full:  
`rsidmap` uses latest dbsnp release (build 155, available at 20210616, >20G for a build) to perform quick search with 
*tabix*.

- Convenient:  
`rsidmap` uses a (tab separated) gwas summary as input and provide output with a new rsid field. 

- Fleasible:  
If you use ANNOVAR, it is [excat map](https://annovar.openbioinformatics.org/en/latest/articles/dbSNP/) (i.e., exact match 
ref, alt). 
`rsidmap` provide a flag `--exact_map` to chose if you want exact match or not, default is False.  
In cross-trait analysis, two alleles can be reordered by taking opposite GWAS effect, so we can only match two alleles (neglecting their orders).

# Requirements
- `Linux` with `wget` and `tabix`
- `Python3` (my version is 3.9.6) with `numpy` (my version is 1.23.1) and `argparse` (my version is 1.1)


## Getting Started
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
`--file_gwas` tab[\t] separated input file  
`--file_out` output file  

Two examples (hg19 and hg38):

```
python ./code/rsidmap.py \
--build hg19 \
--chr_col CHR \
--pos_col POS \
--ref_col A2 \
--alt_col A1 \
--file_gwas ./example/df_hg19.txt \
--file_out ./example/df_hg19_withrsid.txt

python ./code/rsidmap.py \
--build hg38 \
--chr_col chrom \
--pos_col pos \
--ref_col ref \
--alt_col alt \
--file_gwas ./example/df_hg38.txt \
--file_out ./example/df_hg38_withrsid.txt
```

The input file is like:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035
12      104289454       T       C       0.534   0.0085  0.0088  0.3322
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256
4       163471758       T       C       0.612   0.0119  0.0094  0.2057
```

If rsmap is running, you will see:
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
We recommend to use False, i.e., when we found rsid from dbsnp, order of alleles would be neglected. set exact_map as False 
can increase sample size in cross-trait analysis. Because you can reorder two alleles by taking opposite effect in most 
analysis.
process 2/2001
process 4/2001
process 6/2001
process 8/2001
...
```

If rsmap finnised, you will see number of snp map to dbsnp:
```
N. rsid maped: 1722, done!
spend 104.76 sec
```

The output file is like:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P       SNP
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101  rs13387171
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397 rs13175391
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035 rs58796836
12      104289454       T       C       0.534   0.0085  0.0088  0.3322  rs9888379
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256 rs182678857
4       163471758       T       C       0.612   0.0119  0.0094  0.2057  4:163471758:C:T
```
Note that pseudo ids (CHR:POS:REF:ALT) would be added if not matched, see list line above.

## Acknowledgement
Thank Dr. Guowang Lin for his inspiration.

## Feedback and comments
Feel free to add a issue or contact me via zhanghaoyang0@hotmail.com