import argparse
import pickle
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Create histogram of age group mentions.')
parser.add_argument('--pickle',
                    type=argparse.FileType('r'),
                    required=True,
                    help="path to pickled nx graph")
parser.add_argument('--terms',
                    type=argparse.FileType('r'),
                    required=True,
                    help="list of terms for bar chart")
parser.add_argument('--output',
                    type=argparse.FileType('w'),
                    required=True,
                    help="path to output PNG")

args = parser.parse_args()

g = pickle.load(args.pickle)

ag = []
for t in args.terms.readlines():
        term = t.strip()
        ag.append(term)

count = {term:0 for term in ag}

for n in g.nodes():
    if n.term in ag:
        count[n.term] = n.get_weight()

plt.barh(np.arange(len(ag)),
         [count[t] for t in ag],         
         align='center', alpha=0.4)
plt.yticks(np.arange(len(ag)), ag)
plt.tight_layout(pad=2)
plt.xlabel('Menciones')
plt.savefig(args.output)
