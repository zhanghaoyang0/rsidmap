### not run
### this script is for me to check something


### add soft link of dbsnpV155
rm -rf dbsnpV155; ln -s ../db/dbsnpV155 ./dbsnpV155 # link to in-house dbsnp
rm -rf dbsnpV155; mkdir dbsnpV155; touch dbsnpV155/test # make empty fold


### check module version
from importlib_metadata import version
print(version('numpy'))
print(version('argparse '))