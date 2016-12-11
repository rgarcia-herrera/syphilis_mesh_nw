#!/bin/bash



source /srv/home/rgarcia/python_envs/syphilis/bin/activate

`$@`

# echo "creating pickle"
# python ../pubmed_timeline/bin/pubmed_graph_for_year.py \
# 	     --start_year $1 \
# 	     --thru_year $2 \
# 	     --mode $3 \
# 	     --top $4 \
# 	     --ignore syphilis_ignore.txt \
# 	     --groups syphilis_groups.json \
# 	     --pickle $5 \
# 	     --medline syphilis_pubmed.medline


# echo "plotting pickle"
# plot_nx_graph.py --pickle $5 --svg $6
