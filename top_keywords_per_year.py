from pattern.vector import Document
from Bio import Medline
import time, datetime
from pprint import pprint
import json

records = Medline.parse( open('pubmed_result_syphilis.medline') )

terms = {n:{'kw':[], 'publications':0} for n in range(1817,2017)}

for r in records:

    if not 'EDAT' in r.keys():
        print r
        break
        
    # evenly format dates
    if 'EDAT' in r.keys():
        try:
            conv = time.strptime( r['EDAT'], "%Y/%m/%d %H:%M" )
            date = datetime.datetime(*conv[:6]) # entrez date
        except ValueError:
            conv = time.strptime( r['EDAT'], "%Y/%m/%d" )
            date = datetime.datetime(*conv[:6]) # entrez date

        terms[date.year]['publications']+=1
        
        if 'MH' in r:
            d = Document(r['MH'])
            terms[date.year]['kw']+=[w[1] for w in d.keywords()]

        if 'OT' in r:
            d = Document(r['OT'])
            terms[date.year]['kw']+=[w[1] for w in d.keywords()]

        if len(terms[date.year]['kw']) == 0 and 'TI' in r:
            d = Document(r['TI'])
            terms[date.year]['kw']+=[w[1] for w in d.keywords()]
        elif 'AB' in r:
            d = Document(r['AB'])
            terms[date.year]['kw']+=[w[1] for w in d.keywords()]

top_terms = {n:{'kw':[], 'publications':0} for n in range(1817,2017)}
for year in terms:
    d=Document(terms[year]['kw'])
    top_terms[year]['kw'] = d.keywords(top=10)
    top_terms[year]['publications'] = terms[year]['publications']

# kw = set()
# for year in top_terms:
#     for w in top_terms[year]:
#         kw.add(w[1])

#pprint(terms)
