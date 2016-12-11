#!/usr/bin/env python

import argparse
import pickle
import networkx as nx
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Prune a pickled graph removing anything w=1')
parser.add_argument('--pickle',
                    type=argparse.FileType('r'),
                    required=True,
                    help="path to pickled nx graph")
parser.add_argument('--out',
                    type=argparse.FileType('w'),
                    required=True,
                    help="path to output pruned graph")

args = parser.parse_args()
g = pickle.load(args.pickle)

for e in g.edges():
    if g.get_edge_data(*e)['w'] <= 1:
        g.remove_edge(*e)        

for n in g.nodes():
    if g.node[n]['w'] == 1 or len(g.neighbors(n)) < 1:
        g.remove_node(n)

pickle.dump(g, args.out)
