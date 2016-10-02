import svgwrite


class River:
    def __init__(self, filename):
        self.dwg = svgwrite.Drawing(filename=filename)


class Race:
    def __init__(self, fill='grey', marshes={}):
        self.dwg = svgwrite.Drawing(filename='prueba.svg')
        self.marshes = marshes
        self.x = 100
        self.fill = fill

    def add_marsh(self, distance, offset, width,  label=''):
        self.marshes[distance] = {'label': label,
                                  'w': width,
                                  'x': offset}

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
                                  style="font-size: 20")
                self.dwg.add(l)
