from pattern.vector import Document
from Bio import Medline
import time, datetime
from pprint import pprint
import json

uninteresting_terms = ['Humans', 'Male', 'Female', '1','2','3','4','5','6','7','8','9']

def flatten_MH(MH):
    mh = []
    for term in MH:
        words = term.split('/')
        for w in words:
            if w not in uninteresting_terms:
                mh.append(w.replace('*',''))
    return mh

records = Medline.parse( open('pubmed_result_syphilis.medline') )
terms = {n:{'kw':[], 'publications':0} for n in range(1817,2017)}

for r in records:

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
            d = Document(flatten_MH(r['MH']))
            terms[date.year]['kw']+=[w[1] for w in d.keywords()]

        if 'OT' in r:
            d = Document(flatten_MH(r['OT']))
            terms[date.year]['kw']+=[w[1] for w in d.keywords()]

        # no MH or OT? 
        if 'OT' not in r and 'MH' not in r:
            # grab terms from title or abstract
            d = Document(r.get('TI',r.get('AB')))
            kw = []
            for w in d.keywords():
                try:
                    # numbers are uninteresting
                    int(w[1])
                except ValueError:
                    kw.append(w[1])
            terms[date.year]['kw']+= kw

top_terms = {n:{'kw':[], 'publications':0} for n in range(1817,2017)}
for year in terms:
    top_terms[year]['publications'] = terms[year]['publications']
    if top_terms[year]['publications']/20 <= 10:
        top = 10
    else:
        top = top_terms[year]['publications']/20 # top 5%
        
    d=Document(terms[year]['kw'])
    top_terms[year]['kw'] = d.keywords(top=top)


# kw = set()
# for year in top_terms:
#     for w in top_terms[year]:
#         kw.add(w[1])

#pprint(terms)
