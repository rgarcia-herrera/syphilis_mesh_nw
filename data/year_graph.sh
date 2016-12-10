#!/bin/bash

source ~/.virtualenvs/nb/bin/activate

xzcat syphilis_pubmed.medline.xz \
    | python ../pubmed_timeline/bin/pubmed_graph_for_year.py \
	     --start_year $1 \
	     --thru_year $2 \
	     --mode $3 \
	     --ignore syphilis_ignore.txt \
	     --top $4 \
	     --pickle $5

plot_nx_graph.py --pickle $5 --svg $6
