from timeline import Year
from timeline import Citation
import distance
from itertools import combinations
from Bio import Medline
from math import log
from pprint import pprint
import csv
import datetime
import pandas as pd
import numpy as np
import random

records = Medline.parse(open('syphilis_pubmed.medline'))
#records = Medline.parse(open('fixture.medline'))

terms = {n: Year(n) for n in range(1817, 2017)}
all_kw = set()

for r in records:
    # discard 0.9
    if random.random() > 0.1:
        continue
    
    c = Citation(r)
    kw = c.get_meshterms()
    if len(kw.keys()) == 0:
        kw = c.get_keywords()

    terms[c.date.year].add_ref(r.get('PMID'), kw)

all_kw = set.union(*[terms[y].get_keywords() for y in range(1817, 2017)])

all_kw = sorted(list(all_kw))

data = []
for year in range(1817,2017):
    nt = terms[year].get_normalized_kw_fq()
    row = [np.log((nt.get(t,0) * len(terms[year].refs))+1)*50 for t in all_kw]
    data.append(row)

index = pd.date_range(start="1817", end="2016", freq='365D')
df = pd.DataFrame(data, index=index, columns=all_kw)


top = df.astype(bool).sum(axis=0).sort_values(ascending=False)
top40 = [kw for kw in top.index[:40]]

df[top40].to_csv('sampled_top40.csv', sep=',', encoding='utf-8', index_label='year')


    
# write csv file of keywords and their usage
# with open('syphilis_all_kw.csv', 'w') as csvfile:
#     w = csv.writer(csvfile)
#     w.writerow(['year', ] + sorted(all_kw))
#     for year in range(1817, 2017):
#         row = [year, ]
#         for kw in sorted(all_kw):
#             width = normalized_terms[year].get(kw, 0) \
#                     * len(terms[year].refs.keys()) \
#                     + 3

#             if width > 3:
#                 row.append("%.2f" % log(width))
#             else:
#                 row.append(0)
#         w.writerow(row)




#exit()

# compute distances among all pairs of keywords
# sdist = {}
# for pair in combinations(all_kw, 2):
#     sdist[pair] = (distance.levenshtein(*pair),
#                    distance.jaccard(*pair))

# # which pairs are really close?
# for pair in sdist:
#     if sdist[pair][0] < 5 and sdist[pair][1] < 0.3:
#         print pair, sdist[pair]
