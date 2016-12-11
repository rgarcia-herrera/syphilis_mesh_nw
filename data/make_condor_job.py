print "executable = syph_env.sh"

plantilla = """
arguments = pubmed_graph_for_year.py \
 	     --start_year {start_year} \
 	     --thru_year {thru_year} \
 	     --mode {mode} \
 	     --top {top} \
 	     --ignore syphilis_ignore.txt \
 	     --groups syphilis_groups.json \
 	     --pickle {pickle} \
 	     --medline syphilis_pubmed.medline

log          = condor_log/{run_id}.log                                                    
output       = condor_log/{run_id}.out
error        = condor_log/{run_id}.err
queue
"""


for y in range(1817, 2017):
    for mode in ['flatmesh',
                 'meshterms',
                 'keywords',
                 'kw+mh',
                 'kw+flatmh']:        
        run_id = "syph_%s_%s" % (y, mode)
        print plantilla.format(start_year=1817,
                               thru_year=y,
                               mode=mode,
                               top=0,
                               pickle="pickles/%s.pickle" % run_id,
                               run_id=run_id)
