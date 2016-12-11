#!/usr/bin/env python

import argparse
import pickle
import networkx as nx
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Plot a pickled graph.')
parser.add_argument('--pickle',
                    type=argparse.FileType('r'),
                    required=True,
                    help="path to pickled nx graph")
parser.add_argument('--pos',
                    type=argparse.FileType('w'),
                    required=True,
                    help="path to output svg")

args = parser.parse_args()

g = pickle.load(args.pickle)
pos = nx.spring_layout(g)

pickle.dump(pos, args.pos)
