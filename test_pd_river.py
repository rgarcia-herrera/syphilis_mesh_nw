import pandas as pd
from pd_river import River
import argparse

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
args = parser.parse_args()

timeline_df = pd.read_csv(args.csv,
                          parse_dates=['year'], index_col='year')

out_path = args.output.name
args.output.close()
r = River(out_path, timeline_df, args.gap)

print "rendering"

r.to_svg()
r.dwg.save()
