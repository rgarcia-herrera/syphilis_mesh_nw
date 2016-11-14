import svgwrite
import random


class Course():
    label = ""

    def __init__(self, label, fill):
        self.label = label
        self.drains = []
        self.fill = fill
        self.rendered = False

    def drain_at_ofset(self, offset):
        for d in self.drains:
            if d.offset == offset:
                return True
        return False

    def flank_with(self, other, side='right'):
        """ align another course to the edge of self """
        if side == 'right':
            sign = 1
        elif side == 'left':
            sign = -1

        for j in range(len(self.drains)):
            other.drains[j].x = self.drains[j].x \
                                + sign * self.drains[j].width * 0.5 \
                                + sign * other.drains[j].width * 0.5
        other.rendered = True

    def get_source(self):
        """ first drain in the course """
        return sorted(filter(lambda d: d.artificial is False,
                             self.drains),
                      key=lambda d: d.offset)[0]

    def get_sink(self):
        """ last drain """
        return sorted(filter(lambda d: d.artificial is False,
                             self.drains),
                      key=lambda d: d.offset,
                      reverse=True)[0]

    def get_length(self):
        if len(filter(lambda d: d.artificial is False,
               self.drains)) > 2:
            return self.get_sink().offset - self.get_source().offset
        else:
            return 0

    def add_drain(self, drain):
        self.drains.append(drain)
        drain.course = self

    def __repr__(self):
        return "(C %s drains=%s)" % (self.label,
                                     len(self.drains))

    def get_width_at_offset(self, offset):
        if offset < self.get_source().offset \
           or offset > self.get_sink().offset:
            return 0
        elif offset == self.get_source().offset:
            return self.get_source().width
        elif offset == self.get_sink().offset:
            return self.get_sink().width
        else:
            upstream = sorted(filter(lambda d: d.offset < offset
                                     and d.artificial is False,
                                     self.drains),
                              key=lambda d: d.offset)[-1]
            downstream = sorted(filter(lambda d: d.offset > offset
                                       and d.artificial is False,
                                       self.drains),
                                key=lambda d: d.offset)[0]
            width_differential = downstream.width - upstream.width
            local_offset = offset - upstream.offset
            distance = downstream.offset - upstream.offset
            norm_offset = local_offset / distance
            return (width_differential * norm_offset) + upstream.width

    def svg_paths(self, dwg):
        self.paths = []
        control_distance = 0.5
        sorted_drains = sorted(self.drains,
                               key=lambda d: d.offset)

        for n in range(len(sorted_drains)-1):
            d1 = sorted_drains[n]
            d2 = sorted_drains[n+1]

            # render all drains between source and sink, real and artificial
            if d1.offset >= self.get_source().offset \
               and d1.offset < self.get_sink().offset \
               and d2.offset > self.get_source().offset \
               and d2.offset <= self.get_sink().offset:

                x1 = d1.x - (d1.width/2.0)
                y1 = d1.offset

                x2 = d2.x - (d2.width/2.0)
                y2 = d2.offset

                c1x = x1
                c1y = y1 + ((y2-y1)*control_distance)

                c2x = x2
                c2y = y2 - ((y2-y1)*control_distance)

                x3 = d2.x + (d2.width/2.0)
                y3 = d2.offset

                x4 = d1.x + (d1.width/2.0)
                y4 = d1.offset

                c3x = x3
                c3y = y3 - ((y3-y4)*control_distance)

                c4x = x4
                c4y = y4 + ((y2-y1)*control_distance)

                p = dwg.path(d="M%d,%d Z" % (x1, y1),
                             fill=self.fill,
                             stroke=self.fill,
                             stroke_width=1)

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

                dwg.add(p)
            else:
                print "achisachis"

    def center_at(self, x):
        for d in self.drains:
            d.x = x
        self.rendered = True

class Drain():
    x = 0
    width = 0
    offset = 0
    course = None

    def __init__(self, offset, width, artificial=False):
        self.width = width
        self.offset = offset
        self.artificial = artificial

    def __repr__(self):
        if self.artificial:
            a = ' a'
        else:
            a = ''
        return "<o%s x%s w%s%s>" % (self.offset,
                                    self.x,
                                    self.width,
                                    a)


class River():

    def load_courses_from_df(self, df):
        for i, row in df.iteritems():
            y = 10
            c = Course(label=i, fill=random_color())
            for w in df[i].values:
                if w > 0:
                    d = Drain(offset=y, width=w)
                    c.add_drain(d)
                y += 30
            self.courses.append(c)

    def __init__(self, path, dataframe):
        self.courses = []
        self.load_courses_from_df(dataframe)
        self.match_drains() 
        self.get_longest_course().center_at(self.get_max_width() * 0.5 + 30)
        self.centralize_current()
        self.dwg = svgwrite.Drawing(filename=path)

    def match_drains(self):
        """ create artificial drains on courses
        so that all courses have all drains,
        that they may be aligned """

        natural_drains = []
        for c in self.courses:
            natural_drains += filter(lambda d: d.artificial is False, c.drains)

        # add artificial drains where needed
        for d in natural_drains:
            for c in self.courses:
                if d.course is not c and not c.drain_at_ofset(d.offset):
                    c.add_drain(Drain(offset=d.offset,
                                      width=c.get_width_at_offset(d.offset),
                                      artificial=True))

    def to_svg(self):
        for c in self.courses:
            c.svg_paths(self.dwg)

    def center_align_all_courses(self, margin=100):
        center = margin + self.get_max_width() * 0.5
        for c in self.courses:
            c.center_at(center)

    def get_all_drains(self):
        drains = list()
        for c in self.courses:
            for d in c.drains:
                drains.append(d)
        return drains

    def get_rightmost_course(self):
        return sorted(filter(lambda d: d.course.rendered,
                             self.get_all_drains()),
                      key=lambda d: d.x + (d.width * 0.5),
                      reverse=True)[0].course

    def get_leftmost_course(self):
        return sorted(filter(lambda d: d.course.rendered,
                             self.get_all_drains()),
                      key=lambda d: d.x + (d.width * 0.5),
                      reverse=False)[0].course

    def get_max_width(self):
        widths = {}
        for d in self.get_all_drains():
            if d.offset in widths:
                widths[d.offset] += d.width
            else:
                widths[d.offset] = d.width
        return sorted(widths.values())[-1]

    def get_longest_course(self):
        return sorted(self.courses,
                      key=lambda c: c.get_length())[-1]

    def centralize_current(self):
        # iteration count for swinging between right and left
        n = 1

        # longest course is set at the center at init
        for outer in sorted(filter(lambda c: c.rendered is False,
                                   self.courses),
                            key=lambda c: c.get_length(),
                            reverse=True):
            if n % 2:
                side = 'left'
                inner = self.get_leftmost_course()
            else:
                side = 'right'
                inner = self.get_rightmost_course()
            print "%s flanking %s with %s" % (side, inner, outer)
            inner.flank_with(outer, side)
            n += 1



def random_color():
    return random.choice(['red', 'green', 'blue', 'orange', 'aliceblue',
                          'aqua', 'aquamarine', 'azure', 'bisque',
                          'blanchedalmond', 'blueviolet', 'brown',
                          'burlywood', 'cadetblue', 'chartreuse',
                          'chocolate', 'coral', 'cornflowerblue',
                          'crimson', 'darkblue', 'darkcyan',
                          'darkgoldenrod', 'darkgray', 'darkgreen',
                          'darkgrey', 'darkkhaki', 'darkmagenta',
                          'darkolivegreen', 'darkorange',
                          'darkorchid', 'darkred', 'darksalmon',
                          'darkseagreen', 'darkslateblue',
                          'darkslategray', 'darkslategrey',
                          'darkturquoise', 'darkviolet', 'deeppink',
                          'deepskyblue', 'dimgray', 'dimgrey',
                          'dodgerblue', 'firebrick', 'forestgreen',
                          'gainsboro', 'gold', 'goldenrod', 'hotpink',
                          'indianred', 'indigo', 'khaki', 'lavender'])
