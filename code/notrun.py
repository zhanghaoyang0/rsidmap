### not run
### this script is for me to check something

### add soft link of dbsnpV155
rm -rf dbsnp_v155; ln -s ../db/dbsnp_v155 ./dbsnp_v155 # link to in-house dbsnp
rm -rf dbsnp_v155; mkdir dbsnp_v155; touch dbsnp_v155/test # make empty fold


### check module version
from importlib_metadata import version
print(version('numpy'))
print(version('argparse '))