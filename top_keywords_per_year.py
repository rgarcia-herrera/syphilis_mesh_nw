from timeline import Year
from timeline import Citation
import distance
from itertools import combinations
from pattern.vector import Document
from Bio import Medline
import time, datetime
from pprint import pprint
import json
import csv

records = Medline.parse(open('syphilis_pubmed.medline'))
#records = Medline.parse(open('try.medline'))
#terms = {n: {'freq': {}, 'publications': 0} for n in range(1817, 2017)}
terms = {n: Year(n) for n in range(1817, 2017)}
all_kw = set()

for r in records:
    c = Citation(r)
    kw = c.get_meshterms()
    if len(kw.keys()) == 0:
        kw = c.get_keywords()

    terms[c.date.year].add_ref(r.get('PMID'), kw)

    # add them to global kw set
    for w in kw:
        all_kw.add(w)

normalized_terms = dict()
for year in terms:
    normalized_terms[year] = terms[year].get_normalized_kw_fq()


# TODO: writing years as rows allows for nice pandas usage
# write csv file of keywords and their usage
with open('syphilis_all_kw.csv', 'w') as csvfile:
    w = csv.writer(csvfile)
    w.writerow(['kw',] + range(1817, 2017))
    for kw in sorted(all_kw):
        row = [kw, ]
        for year in range(1817, 2017):
            row.append(normalized_terms[year].get(kw, 0) * len(terms[year].refs.keys()))
        if len(row) - row.count(0) > 30: # at least appear 29 times
            w.writerow(row)
        

# top_terms = {n: {'kw': [], 'publications': 0} for n in range(1817, 2017)}
# for year in terms:
#     top_terms[year]['publications'] = terms[year]['publications']
#     if top_terms[year]['publications']/20 <= 10:
#         top = 10
#     else:
#         top = top_terms[year]['publications']/20   # top 5%

#     d = Document(terms[year]['kw'])
#     kwords = d.keywords(top=top)

#     top_terms[year]['kw'] = {kw[1]:kw[0] for kw in kwords}


exit(0)
                       
# compute distances among all pairs of keywords
sdist = {}
for pair in combinations(all_kw, 2):
    sdist[pair] = (distance.levenshtein(*pair),
                   distance.jaccard(*pair))

# which pairs are really close?
for pair in sdist:
    if sdist[pair][0] < 5 and sdist[pair][1] < 0.3:
        print pair, sdist[pair]
