import svgwrite


class River:
    def __init__(self, filename):
        self.dwg = svgwrite.Drawing(filename=filename)


class Race:
    def __init__(self, fill='grey', marshes={}):
        self.dwg = svgwrite.Drawing()
        self.marshes = marshes
        self.fill = fill

    def add_marsh(self, distance, offset, width,  label=''):
        self.marshes[distance] = {'label': label,
                                  'w': width,
                                  'x': offset}

    def center_stream(self, x):
        for distance in self.marshes:
            self.marshes[distance]['x'] = x

    def flank(self, race, side="right"):
        for distance in self.marshes:
            race.marshes[distance]['x'] = self.marshes[distance]['x'] + \
                                          (self.marshes[distance]['w'] / 2.0) + \
                                          (race.marshes[distance]['w'] / 2.0)
            
        

    def render(self):
        control_distance = 0.5
        marsh_distances = sorted(self.marshes.keys())
        for n in range(0, len(marsh_distances)-1):
            m1 = self.marshes[marsh_distances[n]]
            m2 = self.marshes[marsh_distances[n+1]]

            x1 = m1['x'] - (m1['w']/2.0)
            y1 = marsh_distances[n]

            x2 = m2['x'] - (m2['w']/2.0)
            y2 = marsh_distances[n+1]

            c1x = x1
            c1y = y1 + ((y2-y1)*control_distance)

            c2x = x2
            c2y = y2 - ((y2-y1)*control_distance)

            x3 = m2['x'] + (m2['w']/2.0)
            y3 = marsh_distances[n+1]

            x4 = m1['x'] + (m1['w']/2.0)
            y4 = marsh_distances[n]

            c3x = x3
            c3y = y3 - ((y3-y4)*control_distance)

            c4x = x4
            c4y = y4 + ((y2-y1)*control_distance)

            p = self.dwg.path(d="M%d,%d Z" % (x1, y1),
                              fill=self.fill,
                              stroke="white",
                              stroke_width=0)

            # connect x1,y1 to x2, y2
            p.push("C %d %d" % (c1x, c1y))
            p.push("%d %d" % (c2x, c2y))
            p.push("%d %d" % (x2, y2))

            # line to x3, y3
            p.push("L %d %d" % (x3, y3))

            # connect x3,y3 to x4, y4
            p.push("C %d %d" % (c3x, c3y))
            p.push("%d %d" % (c4x, c4y))
            p.push("%d %d" % (x4, y4))

            # line from x4, y4 to x1, y1
            p.push("L %d %d" % (x1, y1))
            self.dwg.add(p)

            # place label
            if m1['label'] != '':
                l = self.dwg.text(m1['label'],
                                  insert=(m1['x'], marsh_distances[n]),
                                  style="font-size: 12; text-anchor:middle")
                self.dwg.add(l)


r = River(filename='prueba.svg')

s = Race(fill='limegreen')
s.add_marsh(distance=1, width=120, offset=200)
s.add_marsh(distance=130, width=90, offset=200)
s.add_marsh(distance=177, width=170, offset=200, label='syphilis')
s.add_marsh(distance=250, width=188, offset=200)
s.add_marsh(distance=322, width=80, offset=200, label='1910')
s.add_marsh(distance=400, width=18, offset=200)
s.render()

m = Race(fill='darkgreen')
m.add_marsh(distance=1, width=120, offset=400)
m.add_marsh(distance=130, width=90, offset=400)
m.add_marsh(distance=177, width=170, offset=400, label='mercury')
m.add_marsh(distance=250, width=188, offset=400)
m.add_marsh(distance=322, width=80, offset=400, label='1910')
m.add_marsh(distance=400, width=18, offset=400)

s.flank(m)

m.render()


r.dwg.add(s.dwg)
r.dwg.add(m.dwg)

r.dwg.save()
