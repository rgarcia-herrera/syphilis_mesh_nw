import svgwrite
from pprint import pprint
from random import randrange

class River:
    def __init__(self, filename):
        pass


class Race:
    def __init__(self, dwg, fill='grey'):
        self.marshes = {}
        self.fill = fill
        self.paths = []
        self.dwg = dwg

    def add_marsh(self, distance, x=0, width=0,  label=''):
        self.marshes[distance] = {'label': label,
                                  'w': width,
                                  'x': x}

    def center_stream(self, x):
        for distance in self.marshes:
            self.marshes[distance]['x'] = x

    def update_paths(self):
        self.paths = []
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

            self.paths.append(p)

    def render(self):
        for p in self.paths:
            self.dwg.add(p)


            # # place label
            # if m1['label'] != '':
            #     l = dwg.text(m1['label'],
            #                       insert=(m1['x'], marsh_distances[n]),
            #                       style="font-size: 12; text-anchor:middle")
            #     self.elements.append(p)

    def flank(self, race):
        for distance in self.marshes:
            self.marshes[distance]['x'] = self.marshes[distance]['w'] * 0.5 + \
                                          race.marshes[distance]['x'] + \
                                          race.marshes[distance]['w'] * 0.5

#r = River()
dwg = svgwrite.Drawing(filename='prueba.svg')

sif = Race(dwg, fill='greenyellow')
sif.add_marsh(distance=1, width=randrange(50,110), x=randrange(100, 133))
sif.add_marsh(distance=130, width=randrange(50,110), x=randrange(100, 133))
sif.add_marsh(distance=177, width=randrange(50,110), x=randrange(100, 133))
sif.add_marsh(distance=250, width=randrange(50,110), x=randrange(100, 133))
sif.add_marsh(distance=322, width=randrange(50,110), x=randrange(100, 133))
sif.add_marsh(distance=400, width=randrange(50,110), x=randrange(100, 133))


m = Race(dwg, fill='darkorange')
m.add_marsh(distance=1, width=randrange(40,70))
m.add_marsh(distance=130, width=randrange(40,70))
m.add_marsh(distance=177, width=randrange(40,70), label='mercury')
m.add_marsh(distance=250, width=randrange(40,70))
m.add_marsh(distance=322, width=randrange(40,70), label='1910')
m.add_marsh(distance=400, width=randrange(40,70))

m.flank(sif)


n = Race(dwg, fill='chocolate')
n.add_marsh(distance=1, width=randrange(40,70))
n.add_marsh(distance=130, width=randrange(40,70))
n.add_marsh(distance=177, width=randrange(40,70), label='nitro')
n.add_marsh(distance=250, width=randrange(100))
n.add_marsh(distance=322, width=randrange(100))
n.add_marsh(distance=400, width=randrange(100))

n.flank(m)


o = Race(dwg, fill='teal')
o.add_marsh(distance=1, width=randrange(40,70))
o.add_marsh(distance=130, width=randrange(40,70))
o.add_marsh(distance=177, width=randrange(40,70), label='nitro')
o.add_marsh(distance=250, width=randrange(100))
o.add_marsh(distance=322, width=randrange(100))
o.add_marsh(distance=400, width=randrange(100))

o.flank(n)


sif.update_paths()
sif.render()
m.update_paths()
m.render()
n.update_paths()
n.render()
o.update_paths()
o.render()

dwg.save()
