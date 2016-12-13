from sh import find

print "executable = syph_env.sh"

plantilla = """
arguments = python pickle_stats.py \
             --pickle {pickle}
output    = {run_id}.csv

log          = condor_log/{run_id}.log                                                    
error        = condor_log/{run_id}.err

queue
"""


for p in find('pickles', '-iname', '*pickle'):
    inpath = p.strip()
    run_id = "stats_%s" % inpath.replace('.pickle','')
    print plantilla.format(pickle=inpath,
                           run_id=run_id)


