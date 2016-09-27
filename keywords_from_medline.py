import argparse
from pattern.vector import Document
from Bio import Medline
import time, datetime
from itertools import combinations
from pprint import pprint
import networkx as nx
import sys

parser = argparse.ArgumentParser(description='grab terms from medline')
parser.add_argument('medline', type=argparse.FileType('r'), default=sys.stdin, help="citations file in medline format")

args    = parser.parse_args()

records = Medline.parse( args.medline )

g = nx.Graph()

for r in records:
    
    # evenly format dates
    if 'EDAT' in r.keys():
        try:
            conv = time.strptime( r['EDAT'], "%Y/%m/%d %H:%M" )
            r['EDAT'] = datetime.datetime(*conv[:6]) # entrez date
        except ValueError:
            conv = time.strptime( r['EDAT'], "%Y/%m/%d" )
            r['EDAT'] = datetime.datetime(*conv[:6]) # entrez date
            
        if 'MH' in r:
            pass
        elif 'OT' in r:
            pass
        elif 'TI' in r:
            d = Document(r['TI'])
            print r['EDAT'], [w[1] for w in d.keywords()]
        else:
            d = Document(r['AB'])
            print r['EDAT'], [w[1] for w in d.keywords(top=6)]

