import river

s = river.Race(fill='limegreen')
s.add_marsh(distance=1, width=120, offset=210)
s.add_marsh(distance=130, width=90, offset=50)
s.add_marsh(distance=177, width=170, offset=100, label='syphilis')
s.add_marsh(distance=250, width=188, offset=70)
s.add_marsh(distance=322, width=80, offset=120)
s.add_marsh(distance=400, width=18, offset=200)

s.render()
s.dwg.save()
