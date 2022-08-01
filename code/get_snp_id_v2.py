import sys
import time
import gzip

bim = sys.argv[1]
db_snp = sys.argv[2]

start = time.time()

with open(bim) as f:
    bim_pos = {tuple(i[:2]) for i in (line.split() for line in f)}

i = 1
start = time.time()
with gzip.open(db_snp, 'rt') as f:  # dbSNP line in bim position
    share_db_line = {tuple(i[:2]): i[2:] for i in (line.split() for line in f) if tuple(i[:2]) in bim_pos}
end = time.time()
end - start 
# 1673.6871206760406



with open(bim) as f:
    for line in f:
        parts = line.split()
        token = tuple(parts[:2])
        snp = parts[-1]
        if token in share_db_line:
            db_row = share_db_line[token]  # snp_id, a1, a2
            if set(db_row[-2:]) == set(parts[2:4]):
                snp = db_row[0]
        print(*parts, snp, sep='\t')

end = time.time()
print(end - start)
