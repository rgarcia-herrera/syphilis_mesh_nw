# s = Race(color='yellow')

# s.add_recess(distance=1817, width=50)
# s.add_recess(distance=1842, width=200)


# r = River()

# r.add_race(s)
# r.add_race(s)



# for y in terms:
#     if 'syphilis' in terms[y]:
#         r=Recess()



dwg = svgwrite.Drawing('aguas.svg')

p = dwg.path(d="M10,10 Z",
             fill="#00ff00",
             stroke="red",
             stroke_width=6)

p.push("C 50 100")
p.push("50 100")
p.push("100 10")

dwg.add(p)
dwg.save()
