
plantilla = """
executable = year_graph.sh

arguments = {start_year} \
            {thru_year} \
            {mode} \
            {top} \
            {pickle} \
            {svg}

log        = {run_id}.log                                                    
output       = {run_id}.out
error        = {run_id}.err
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
                               top=20,
                               pickle="pickles/%s.pickle" % run_id,
                               svg="plots/%s.svg" % run_id,
                               run_id=run_id)
