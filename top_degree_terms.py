from timeline import Term
from timeline import Citation
from Bio import Medline
import networkx as nx
import itertools
import operator
import pandas as pd
import numpy as np
import json
import argparse

from pprint import pprint

parser = argparse.ArgumentParser(description='Create timeline of keyword "volumes" in CSV file.')
parser.add_argument('--medline',
                    type=argparse.FileType('r'),
                    required=True,
                    help="citations file in medline format")
parser.add_argument('--start_year',
                    type=int,
                    required=True,
                    help="start year of timeline")
parser.add_argument('--thru_year',
                    type=int,
                    required=True,
                    help="end year of timeline")
parser.add_argument('--mode',
                    choices=['flatmesh',
                             'meshterms',
                             'keywords',
                             'kw+mh',
                             'kw+flatmh'],
                    default='both',
                    help="extract mesh-terms, keywords or both")

parser.add_argument('--groups',
                    type=argparse.FileType('r'),
                    required=False,
                    help="dictionary that groups similar terms, in json format")

parser.add_argument('--ignore',
                    type=argparse.FileType('r'),
                    required=False,
                    help="file with list of terms to remove from network")

parser.add_argument('--top',
                     type=int,
                     default=40,
                     help="how many top terms")
parser.add_argument('--output',
                    type=argparse.FileType('w'),
                    required=True,
                    help="path to output csv")

args = parser.parse_args()

if args.groups:
    group_terms = json.load(args.groups)
else:
    group_terms = {}
    
records = Medline.parse(args.medline)

G = nx.Graph()
all_terms = dict()

for r in records:
    c = Citation(r)
    if args.mode == 'meshterms':
        local_terms = c.get_meshterms(flatten=False, groups=group_terms)
    elif args.mode == 'flatmesh':
        local_terms = c.get_meshterms(flatten=True, groups=group_terms)        
    elif args.mode == 'keywords':
        local_terms = c.get_keywords(groups=group_terms)
    elif args.mode == 'kw+mh':
        local_terms = c.get_keywords(groups=group_terms) + c.get_meshterms(flatten=False, groups=group_terms)
    elif args.mode == 'kw+flatmh':
        local_terms = c.get_keywords(groups=group_terms) + c.get_meshterms(flatten=True, groups=group_terms)

        
    for term in local_terms:
        if term in all_terms:
            if c.date.year in all_terms[term].mentions_in_year:
                all_terms[term].mentions_in_year[c.date.year] += 1
            else:
                all_terms[term].mentions_in_year[c.date.year] = 1
        else:
            all_terms[term] = Term(term)
            all_terms[term].mentions_in_year[c.date.year] = 1

    for pair in itertools.combinations(local_terms, 2):
        n0 = all_terms[pair[0]]
        n1 = all_terms[pair[1]]
        w = G.get_edge_data(n0, n1, default={'w':1})
        G.add_edge(n0, n1, w)


# remove uninteresting terms
if args.ignore:
    for t in args.ignore.readlines():
        term = t.strip()
        if term in all_terms:
            G.remove_node(all_terms[term])

degree_sorted = sorted(G.degree(weight='w').items(), key=operator.itemgetter(1))
#degree_sorted = sorted(nx.betweenness_centrality(G, weight='w').items(), key=operator.itemgetter(1))
degree_sorted.reverse()

top = [t[0] for t in degree_sorted[:args.top]]

data = []
for year in range(args.start_year, args.thru_year + 1):
    row = [np.log10(t.mentions_in_year.get(year, 1))*10 for t in top]
    data.append(row)

index = pd.date_range(start=str(args.start_year),
                      end=str(args.thru_year),
                      freq='365D')
df = pd.DataFrame(data, index=index, columns=[t.term for t in top])

df.to_csv(args.output,
          sep=',',
          encoding='utf-8',
          index_label='year')
