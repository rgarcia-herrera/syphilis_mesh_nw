import distance
from itertools import combinations
from pattern.vector import Document
from Bio import Medline
import time, datetime
from pprint import pprint
import json
import csv

uninteresting_terms = ['Humans', 'Male', 'Female', ]


def flatten_MH(MH):
    mh = []
    for term in MH:
        words = term.split('/')
        for w in words:
            if w not in uninteresting_terms:
                mh.append(w.replace('*', ''))
    return mh

records = Medline.parse(open('syphilis_pubmed.medline'))
terms = {n: {'kw': [], 'publications': 0} for n in range(1817, 2017)}

for r in records:

    if 'EDAT' in r.keys():
        # evenly format dates
        try:
            conv = time.strptime(r['EDAT'], "%Y/%m/%d %H:%M")
            date = datetime.datetime(*conv[:6])  # entrez date
        except ValueError:
            conv = time.strptime(r['EDAT'], "%Y/%m/%d")
            date = datetime.datetime(*conv[:6])  # entrez date

        terms[date.year]['publications'] += 1

        if 'MH' in r:
            d = Document(flatten_MH(r['MH']))
            terms[date.year]['kw'] += [w[1] for w in d.keywords()]
        elif 'OT' in r:
            d = Document(flatten_MH(r['OT']))
            terms[date.year]['kw'] += [w[1] for w in d.keywords()]
            continue
        # no MH or OT?
        elif 'OT' not in r and 'MH' not in r:
            # grab terms from title or abstract
            d = Document(r.get('TI', r.get('AB')))
            kw = []
            for w in d.keywords():
                try:
                    # numbers are uninteresting
                    int(w[1])
                except ValueError:
                    kw.append(w[1])
            terms[date.year]['kw'] += kw

            
top_terms = {n: {'kw': [], 'publications': 0} for n in range(1817, 2017)}
for year in terms:
    top_terms[year]['publications'] = terms[year]['publications']
    if top_terms[year]['publications']/20 <= 10:
        top = 10
    else:
        top = top_terms[year]['publications']/20   # top 5%

    d = Document(terms[year]['kw'])
    kwords = d.keywords(top=top)

    top_terms[year]['kw'] = {kw[1]:kw[0] for kw in kwords}

    
# create set with all the keywords
all_kw = set()
for year in top_terms:
    for kw in top_terms[year]['kw'].keys():
        all_kw.add(kw)



# write csv file of keywords and their usage
with open('top_kw.csv', 'w') as csvfile:
    w = csv.writer(csvfile)
    w.writerow(['kw',] + sorted(top_terms.keys()))
    for kw in sorted(all_kw):
        row = [kw, ]
        for year in top_terms:
            if kw in top_terms[year]['kw']:
                row.append(top_terms[year]['kw'][kw] * top_terms[2016]['publications'] )
            else:
                row.append(0)
        w.writerow(row)

        
# compute distances among all pairs of keywords
sdist = {}
for pair in combinations(all_kw, 2):
    sdist[pair] = (distance.levenshtein(*pair),
                   distance.jaccard(*pair))

# which pairs are really close?
for pair in sdist:
    if sdist[pair][0] < 5 and sdist[pair][1] < 0.3:
        print pair, sdist[pair]
