nets = [
    'pickles/syph_1945_meshterms_pruned.pickle',
    'pickles/syph_1960_meshterms_pruned.pickle',
    'pickles/syph_1975_meshterms_pruned.pickle',
    'pickles/syph_1990_meshterms_pruned.pickle',
    'pickles/syph_2005_meshterms_pruned.pickle',
    'pickles/syph_2016_meshterms_pruned.pickle',

    'pickles/syph_1945_flatmesh_pruned.pickle',
    'pickles/syph_1960_flatmesh_pruned.pickle',
    'pickles/syph_1975_flatmesh_pruned.pickle',
    'pickles/syph_1990_flatmesh_pruned.pickle',
    'pickles/syph_2005_flatmesh_pruned.pickle',
    'pickles/syph_2016_flatmesh_pruned.pickle',

    'pickles/syph_1945_kw+mh_pruned.pickle',
    'pickles/syph_1960_kw+mh_pruned.pickle',
    'pickles/syph_1975_kw+mh_pruned.pickle',
    'pickles/syph_1990_kw+mh_pruned.pickle',
    'pickles/syph_2005_kw+mh_pruned.pickle',
    'pickles/syph_2016_kw+mh_pruned.pickle',

    'pickles/syph_1945_kw+flatmh_pruned.pickle',
    'pickles/syph_1960_kw+flatmh_pruned.pickle',
    'pickles/syph_1975_kw+flatmh_pruned.pickle',
    'pickles/syph_1990_kw+flatmh_pruned.pickle',
    'pickles/syph_2005_kw+flatmh_pruned.pickle',
    'pickles/syph_2016_kw+flatmh_pruned.pickle',
    
]
              
print "executable = syph_env.sh"

plantilla = """
arguments = python pickle2edgelist.py --pickle {pickle} 
output    = edgelists/{edgelist}

log       = condor_log/{run_id}.log                                                    
error     = condor_log/{run_id}.err
queue
"""

for p in nets:
    inpath = p.strip()
    outpath = inpath.replace('.pickle', '.edgelist')
    run_id = "el_%s" % inpath.replace('.pickle','')
    print plantilla.format(pickle=inpath,
                           edgelist=outpath,
                           run_id=run_id)
