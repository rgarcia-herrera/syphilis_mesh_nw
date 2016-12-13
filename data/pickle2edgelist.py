import argparse
import networkx as nx

parser = argparse.ArgumentParser(description='Export pickled nx graph to a comma separated edgelist.')
parser.add_argument('--pickle', type=argparse.FileType('r'), required=True )
args   = parser.parse_args()

h = nx.read_gpickle( args.pickle )

for e in h.edges():
    (s, t) = e
    l = ";".join([s,
                  str(h.node[s]['w']),
                  t,
                  str(h.node[t]['w']),
                  str(h.get_edge_data(*e)['w'])])
    print l.encode('utf8')
