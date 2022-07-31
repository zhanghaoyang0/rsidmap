
# rsidmap
`rsidmap` is a tool for to find rsid with genome postion in a GWAS summary.

# Why rsidmap
- Quick and full:  
`rsidmap` uses latest dbsnp release (build 155, available at 20210616, >20G for a build) to perform quick search with *tabix*.

- Convenient:  
`rsidmap` can use a (tab separated) gwas summary as input and provide another add gwas summar with a new rsid field as output. 

- Fleasible:  
If you use ANNOVAR, it is [excat map](https://annovar.openbioinformatics.org/en/latest/articles/dbSNP/) (i.e., exact match ref, alt). 
In most cross-trait analysis we only want to match two alleles (neglecting their orders), because many software can reorder two alleles (by taking opposite GWAS effect). 
`rsidmap` provide a flag to chose if you want exact match or not.

## Getting Started
Clone this repository via the commands:
```  
git clone https://github.com/zhanghaoyang0/rsidmap.git
cd rsidmap
```

Download latest_release dbsnp with `wget`:
```
wget -c https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.25.gz -P dbsnp/
wget -c https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.39.gz -P dbsnp/
wget -c https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.25.gz.tbi -P dbsnp/
wget -c https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/GCF_000001405.39.gz.tbi -P dbsnp/
```

Once the above has completed, you can try to add rsid field by specifying: 
`--build` hg19 or hg38  
`--chr_col` field name of CHR, default is CHR   
`--pos_col` field name of POS, default is POS  
`--ref_col` field name of REF, default is REF  
`--alt_col` field name of ALT, default is ALT  
`--exact_map` excat map or not, default is False  
`--file_in` tab[\t] separated input file  
`--file_out` output file  

Two examples (hg19 and hg38):

```
python ./code/rsid.py \
--build hg19 \
--chr_col CHR \
--pos_col POS \
--ref_col REF \
--alt_col ALT \
--file_in ./test/df_hg19.txt \
--file_out ./test/df_hg19_withrsid.txt

python ./code/rsid.py \
--build hg38 \
--chr_col chrom \
--pos_col pos \
--ref_col ref \
--alt_col alt \
--file_gwas ./test/df_hg38.txt \
--file_out ./test/df_hg38_withrsid.txt
```

## Feedback and comments
Feel free to add a issue or contact me via zhanghaoyang0@hotmail.com
