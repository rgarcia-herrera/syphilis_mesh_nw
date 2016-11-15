import pandas as pd
from pd_river import Course, Drain, River
import random

timeline_df = pd.read_csv('sampled_top40.csv',
                          parse_dates=['year'], index_col='year')

r = River('sampled_top40.svg', timeline_df)

for c in r.courses:
    print c, c.get_length(), sorted(c.drains, key=lambda x: x.offset)

print "longest", r.get_longest_course()
print "rendering"

r.to_svg()
r.dwg.save()


# by_len = timeline_df.astype(bool).sum(axis=0)
# by_len.sort_values(ascending=False, inplace=True)

# for i, row in by_len.iteritems():
#     print i
