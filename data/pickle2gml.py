import argparse
import networkx as nx

parser = argparse.ArgumentParser(description='Export pickled nx graph to GML.')
parser.add_argument('--pickle', type=argparse.FileType('r'), required=True )
parser.add_argument('--gml', type=argparse.FileType('w'), required=True )
args   = parser.parse_args()

h = nx.read_gpickle( args.pickle )

nx.write_gml(h,
             args.gml)
