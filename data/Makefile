all: syphilis_flatmesh_grouped_top300.csv syphilis_meshterms_grouped_top300.csv syphilis_keywords_grouped_top300.csv syphilis_kw+mh_grouped_top300.csv syphilis_kw+flatmh_grouped_top300.csv syphilis_flatmesh_top300.csv syphilis_meshterms_top300.csv syphilis_keywords_top300.csv syphilis_kw+mh_top300.csv syphilis_kw+flatmh_top300.csv syphilis_terms_flatmesh_grouped_top300.txt syphilis_terms_meshterms_grouped_top300.txt syphilis_terms_keywords_grouped_top300.txt syphilis_terms_kw+mh_grouped_top300.txt syphilis_terms_kw+flatmh_grouped_top300.txt syphilis_terms_flatmesh_top300.txt syphilis_terms_meshterms_top300.txt syphilis_terms_keywords_top300.txt syphilis_terms_kw+mh_top300.txt syphilis_terms_kw+flatmh_top300.txt 

clean:
	rm -f syphilis_*top300.csv
	rm -f syphilis_terms_*top300.txt

syphilis_terms_flatmesh_grouped_top300.txt: syphilis_flatmesh_grouped_top300.csv
	head -n 1 syphilis_flatmesh_grouped_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_flatmesh_grouped_top300.txt

syphilis_terms_meshterms_grouped_top300.txt: syphilis_meshterms_grouped_top300.csv
	head -n 1 syphilis_meshterms_grouped_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_meshterms_grouped_top300.txt

syphilis_terms_keywords_grouped_top300.txt: syphilis_keywords_grouped_top300.csv
	head -n 1 syphilis_keywords_grouped_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_keywords_grouped_top300.txt

syphilis_terms_kw+mh_grouped_top300.txt: syphilis_kw+mh_grouped_top300.csv
	head -n 1 syphilis_kw+mh_grouped_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_kw+mh_grouped_top300.txt

syphilis_terms_kw+flatmh_grouped_top300.txt: syphilis_kw+flatmh_grouped_top300.csv
	head -n 1 syphilis_kw+flatmh_grouped_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_kw+flatmh_grouped_top300.txt

syphilis_terms_flatmesh_top300.txt: syphilis_flatmesh_top300.csv
	head -n 1 syphilis_flatmesh_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_flatmesh_top300.txt

syphilis_terms_meshterms_top300.txt: syphilis_meshterms_top300.csv
	head -n 1 syphilis_meshterms_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_meshterms_top300.txt

syphilis_terms_keywords_top300.txt: syphilis_keywords_top300.csv
	head -n 1 syphilis_keywords_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_keywords_top300.txt

syphilis_terms_kw+mh_top300.txt: syphilis_kw+mh_top300.csv
	head -n 1 syphilis_kw+mh_top300.csv | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_kw+mh_top300.txt

syphilis_terms_kw+flatmh_top300.txt : syphilis_kw+flatmh_top300.csv 
	head -n 1 syphilis_kw+flatmh_top300.csv  | sed 's/;/\n/g' | tail -n +2 > syphilis_terms_kw+flatmh_top300.txt




syphilis_flatmesh_grouped_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode flatmesh \
				     --groups syphilis_groups.json \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_flatmesh_grouped_top300.csv

syphilis_meshterms_grouped_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode meshterms \
				     --groups syphilis_groups.json \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_meshterms_grouped_top300.csv

syphilis_keywords_grouped_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode keywords \
				     --groups syphilis_groups.json \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_keywords_grouped_top300.csv

syphilis_kw+mh_grouped_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode kw+mh \
				     --groups syphilis_groups.json \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_kw+mh_grouped_top300.csv

syphilis_kw+flatmh_grouped_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode kw+flatmh \
				     --groups syphilis_groups.json \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_kw+flatmh_grouped_top300.csv











syphilis_flatmesh_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode flatmesh \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_flatmesh_top300.csv

syphilis_meshterms_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode meshterms \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_meshterms_top300.csv

syphilis_keywords_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode keywords \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_keywords_top300.csv

syphilis_kw+mh_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode kw+mh \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_kw+mh_top300.csv

syphilis_kw+flatmh_top300.csv: 
	xzcat syphilis_pubmed.medline.xz \
		| \
		pubmed_timeline_top_degree --start_year 1817 \
				     --thru_year 2017 \
				     --mode kw+flatmh \
				     --ignore syphilis_ignore.txt \
				     --top 300 \
				     --output syphilis_kw+flatmh_top300.csv
