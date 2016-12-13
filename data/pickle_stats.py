import argparse
import networkx as nx

parser = argparse.ArgumentParser(description='Basic network analysis measures.')
parser.add_argument('--pickle', type=argparse.FileType('r'), required=True )
args   = parser.parse_args()

h = nx.read_gpickle( args.pickle )

g = sorted(nx.connected_component_subgraphs(h), key=len, reverse=True)[0]

N, K = g.order(), g.size()
avg_deg = float(K)/N

diameter = nx.diameter(g)

try:
    avg_path_len = nx.average_shortest_path_length(g)
except:
    avg_path_len = "na"


W=[g.node[n]['w'] for n in g.nodes()]
avg_mentions = float(sum(W))/len(W)

W=[g.get_edge_data(*e)['w'] for e in g.edges()]
avg_interaction_w = float(sum(W))/len(W)

# N K avg_deg diameter avg_path_len
print ",".join([str(s) for s in [args.pickle.name, N, K, avg_deg, diameter, avg_path_len, avg_mentions, avg_interaction_w]])
