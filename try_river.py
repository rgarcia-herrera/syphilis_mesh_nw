s = Race(color='yellow')

s.add_recess(distance=1817, width=50)
s.add_recess(distance=1842, width=200)


r = River()

r.add_race(s)
r.add_race(s)



for y in terms:
    if 'syphilis' in terms[y]:
        r=Recess()
