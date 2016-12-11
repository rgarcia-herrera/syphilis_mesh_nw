large_nets = ['pickles/syph_2016_flatmesh_pruned.pickle',
              'pickles/syph_2016_keywords_pruned.pickle',
              'pickles/syph_2016_kw+flatmh_pruned.pickle',
              'pickles/syph_2016_kw+mh_pruned.pickle',
              'pickles/syph_2016_meshterms_pruned.pickle']
              
print "executable = syph_env.sh"

plantilla = """
arguments = ./spring_pos.py \
            --pickle {pickle} \
            --pos {pos}

log          = condor_log/{run_id}.log                                                    
output       = condor_log/{run_id}.out
error        = condor_log/{run_id}.err
queue
"""

for p in large_nets:
    inpath = p.strip()
    outpath = inpath.replace('.pickle', '_pos.pickle')
    run_id = "pos_%s" % inpath.replace('.pickle','')
    print plantilla.format(pickle=inpath,
                           pos=outpath,
                           run_id=run_id)
