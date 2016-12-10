all:
	xzcat syphilis_pubmed.medline.xz | pubmed_timeline_top_degree --start_year 1817 --thru_year 2017 --mode kw+mh --groups syphilis_groups.json --ignore syphilis_ignore.txt --top 300 --output syphilis_kw+mh_grouped_top300.csv --medline -
