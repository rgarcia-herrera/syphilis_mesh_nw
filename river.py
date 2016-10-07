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

    def flank(self, race, side):
        if side == 'r':
            sign = 1
        elif side == 'l':
            sign = -1

        new_marshes = []
        for d in self.marshes:
            if d in race.marshes:
                self.marshes[d]['x'] = sign * self.marshes[d]['w'] * 0.5 + \
                                       race.marshes[d]['x'] + \
                                       sign * race.marshes[d]['w'] * 0.5
            else:
                (closest, quite_close) = race.closest_marshes_to(d)
                # place our discording marsh at the offset of the closest 
                self.marshes[d]['x'] = sign * self.marshes[d]['w'] * 0.5 + \
                                       race.marshes[closest]['x'] + \
                                       sign * race.marshes[closest]['w'] * 0.5
                # create a new marsh at the next to closest distance
                w = self.average_width_at(quite_close)
                new_marshes.append((quite_close,
                                    race.marshes[quite_close]['x'] \
                                    + race.marshes[quite_close]['w'] * 0.5 \
                                    + w * 0.5,
                                    w))

        for new in new_marshes:
            self.add_marsh(*new)
                
    def average_width_at(self, distance):
        diff = {}
        for d in self.marshes:
            diff[abs(distance - d)] = d

        closest = diff[sorted(diff.keys())[0]]

        if distance < closest:
            bottom = self.marshes.keys()[self.marshes.keys().index(closest)-1]
            top = closest
        else:
            top = self.marshes.keys()[self.marshes.keys().index(closest)+1]
            bottom = closest
            
        print bottom, top
        
        return 30
    
    def closest_marshes_to(self, distance):
        diff = {}
        for d in self.marshes:
            diff[abs(distance - d)] = d
        return (diff[sorted(diff.keys())[0]],diff[sorted(diff.keys())[1]])


#r = River()
dwg = svgwrite.Drawing(filename='prueba.svg')

sif = Race(dwg, fill='greenyellow')
sif.add_marsh(distance=1, width=randrange(50, 110), x=randrange(250, 333))
sif.add_marsh(distance=300, width=50, x=randrange(100, 133))
sif.add_marsh(distance=600, width=randrange(50, 110), x=randrange(100, 133))
sif.center_stream(400)

m = Race(dwg, fill='darkorange')
m.add_marsh(distance=1, width=randrange(40,70))
m.add_marsh(distance=280, width=randrange(40,70))
m.add_marsh(distance=500, width=randrange(40,70))
m.add_marsh(distance=680, width=randrange(40,70), label='mercury')
m.flank(sif, 'r')


sif.update_paths()
sif.render()
m.update_paths()
m.render()

dwg.add( dwg.text('300',
             insert=(400,300),
             style="font-size: 12; text-anchor:middle") )

dwg.add( dwg.text('500',
             insert=(400,500),
             style="font-size: 12; text-anchor:middle") )

dwg.save()
