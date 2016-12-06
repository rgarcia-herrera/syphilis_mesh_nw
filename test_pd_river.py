import pandas as pd
from pd_river import River
import argparse
import json

parser = argparse.ArgumentParser(description='Create riverplot from csv timeline')
parser.add_argument('--csv',
                    type=argparse.FileType('r'),
                    required=True,
                    help="csv timeline")
parser.add_argument('--output',
                    type=argparse.FileType('w'),
                    required=True,
                    help="path to output svg")
parser.add_argument('--gap',
                    type=int,
                    default=30,
                    help='space between drains')
parser.add_argument('--layout',
                    type=argparse.FileType('r'),                    
                    required=False,
                    help='json layout file')

args = parser.parse_args()

timeline_df = pd.read_csv(args.csv,
                          parse_dates=['year'], index_col='year')

if args.layout:
    layout = json.load(args.layout)
else:
    layout = {}

out_path = args.output.name
args.output.close()
r = River(out_path,
          timeline_df,
          gap=args.gap,
          layout=layout,
          grid_labels=[t.year for t in timeline_df.index])

print "rendering"

r.to_svg()
r.dwg.save()
