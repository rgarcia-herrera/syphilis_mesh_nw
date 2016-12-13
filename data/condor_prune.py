from sh import find

print "executable = syph_env.sh"

plantilla = """
arguments = ./prune_graph.py \
             --pickle {pickle} \
             --edgeth 20 \
             --out {out}

log          = condor_log/{run_id}.log                                                    
output       = condor_log/{run_id}.out
error        = condor_log/{run_id}.err
queue
"""

for p in find('pickles', '-iname', '*pickle'):
    inpath = p.strip()
    outpath = inpath.replace('.pickle', '_pruned.pickle')
    run_id = "prune_%s" % inpath.replace('.pickle','')
    print plantilla.format(pickle=inpath,
                           out=outpath,
                           run_id=run_id)
