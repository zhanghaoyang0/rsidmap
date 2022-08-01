### not run
### this script is for me to check something

### add soft link of dbsnpV155
rm -rf dbsnp_v155; ln -s ../db/dbsnp_v155 ./dbsnp_v155 # link to in-house dbsnp
rm -rf dbsnp_v155; mkdir dbsnp_v155; touch dbsnp_v155/test # make empty fold


### check module version
from importlib_metadata import version
print(version('argparse'))
print(version('argparse'))

### add some snp to test 
# hg 19
$ tabix GCF_000001405.25.gz NC_000001.10:10054-10055
NC_000001.10    10054   rs1639543798    C       CT      
NC_000001.10    10054   rs1639543820    CT      C      
NC_000001.10    10055   rs768019142     TA      T,TAA  
NC_000001.10    10055   rs892501864     T       A,C    
# hg38
$ tabix GCF_000001405.39.gz NC_000001.11:10054-10055
NC_000001.11    10054   rs1639543798    C       CT     
NC_000001.11    10054   rs1639543820    CT      C       
NC_000001.11    10055   rs768019142     TA      T,TAA  
NC_000001.11    10055   rs892501864     T       A,C     
# add this to test file
1   10054   C   CT  0.2313  0.002   0.23    0.3121
1   10054   CT  C   0.1213  0.042   0.12    0.0031
1   10054   T   A   0.165   0.011    0.63   0.0259
1   10054   T   C   0.151   0.023    0.02   0.0121





