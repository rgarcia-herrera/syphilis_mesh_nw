from timeline import Year
from timeline import Citation
from Bio import Medline
import pandas as pd
import numpy as np
import random
import argparse


parser = argparse.ArgumentParser(description='Create timeline of keyword "volumes" in CSV file.')
parser.add_argument('--medline',
                    type=argparse.FileType('r'),
                    required=True,
                    help="citations file in medline format")
parser.add_argument('--sample',
                    type=float,
                    default=1.0,
                    help="ratio to sample, between 0.0 and 1.0")
parser.add_argument('--start_year',
                    type=int,
                    required=True,
                    help="start year of timeline")
parser.add_argument('--thru_year',
                    type=int,
                    required=True,
                    help="end year of timeline")
parser.add_argument('--scale',
                    type=float,
                    default=10,
                    help="multiply keyword volumes by this")
parser.add_argument('--top',
                    type=int,
                    default=40,
                    help="how many top terms")
parser.add_argument('--output',
                    type=argparse.FileType('w'),
                    required=True,
                    help="path to output csv")

args = parser.parse_args()


records = Medline.parse(args.medline)

terms = {n: Year(n) for n in range(args.start_year, args.thru_year + 1)}
all_kw = set()

for r in records:
    # sample
    if random.random() < 1.0 - args.sample:
        continue

    c = Citation(r)
    if c.date.year in range(args.start_year, args.thru_year + 1):
        kw = c.get_meshterms()
        if len(kw.keys()) == 0:
            kw = c.get_keywords()

            terms[c.date.year].add_ref(r.get('PMID'), kw)

all_kw = set.union(*[terms[y].get_keywords()
                     for y in range(args.start_year, args.thru_year + 1)])

all_kw = sorted(list(all_kw))

data = []
for year in range(args.start_year, args.thru_year + 1):
    nt = terms[year].get_normalized_kw_fq()
    row = [np.log((nt.get(t, 0) * len(terms[year].refs)) + 1)
           * args.scale for t in all_kw]
    data.append(row)

index = pd.date_range(start=str(args.start_year),
                      end=str(args.thru_year),
                      freq='365D')
df = pd.DataFrame(data, index=index, columns=all_kw)

top = df.astype(bool).sum(axis=0).sort_values(ascending=False)
top40 = [w for w in top.index[:args.top]]

df[top40].to_csv(args.output,
                 sep=',',
                 encoding='utf-8',
                 index_label='year')
