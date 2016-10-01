import svgwrite


class River:
    def __init__(self, filename):
        self.dwg = svgwrite.Drawing(filename=filename)


class Race:
    def __init__(self, fill='grey', marshes=[]):
        self.dwg = svgwrite.Drawing(filename='prueba.svg')
        self.marshes = marshes
        self.x = 100
        self.fill = fill

    def add_marsh(self, distance, width):
        self.marshes.append((distance, width))

    def render(self):
        for n in range(0, len(self.marshes)-1):
            print n
            x1 = self.x - (self.marshes[n][1]/2.0)
            y1 = self.marshes[n][0]

            x2 = self.x - (self.marshes[n+1][1]/2.0)
            y2 = self.marshes[n+1][0]

            c1x = x1
            c1y = y1 + ((y2-y1)/3.0)            

            c2x = x2
            c2y = y2 - ((y2-y1)/3.0)            

            x3 = self.x + (self.marshes[n+1][1]/2.0)
            y3 = self.marshes[n+1][0]

            x4 = self.x + (self.marshes[n][1]/2.0)
            y4 = self.marshes[n][0]

            p = self.dwg.path(d="M%d,%d Z" % (x1, y1),
                              fill=self.fill,
                              stroke="red",
                              stroke_width=2)

            # connect x1,y1 to x2, y2
            p.push("C %d %d" % (c1x, c1y))
            p.push("%d %d" % (c2x, c2y))
            p.push("%d %d" % (x2, y2))

            self.dwg.add(p)



# dwg = svgwrite.Drawing('aguas.svg')

# p = dwg.path(d="M10,10 Z",
#              fill="#00ff00",
#              stroke="red",
#              stroke_width=6)

# p.push("C 30 10")
# p.push("30 30")
# p.push("0 50")

# dwg.add(p)
# dwg.save()


s = Race(fill='yellow')

s.add_marsh(distance=1, width=20)
s.add_marsh(distance=100, width=80)

s.render()
s.dwg.save()
