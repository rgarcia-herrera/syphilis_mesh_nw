from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, \
    Boolean, create_engine, ForeignKey
from sqlalchemy.orm import relationship
import svgwrite


Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    label = Column(String(200), nullable=True)
    length = Column(Float, default=0)
    drains = relationship(lambda:Drain,
                          order_by=lambda: Drain.offset,
                          back_populates="course")

    # first drain
    def get_source(self):
        return filter(lambda d: d.artificial is False,
                      self.drains)[0]

    # last drain
    def get_sink(self):
        return filter(lambda d: d.artificial is False,
                      self.drains)[-1]

    def update_length(self):
        if len(filter(lambda d: d.artificial is False,
               self.drains)) > 2:
            self.length = self.get_sink().offset - self.get_source().offset
        else:
            self.length = 0

    def add_drain(self, drain):
        self.drains.append(drain)
        self.update_length()
        session.commit()

    def __repr__(self):
        self.update_length()
        return "~~ %s len=%s drains=%s" % (self.label,
                                                 self.length,
                                                 len(self.drains))

    def get_width_at_offset(self, offset):
        if offset < self.get_source().offset \
           or offset > self.get_sink().offset:
            return 0
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

    def svg_paths(self, dwg, fill='grey'):
        self.paths = []
        control_distance = 0.5
        sorted_drains = sorted(self.drains,
                               key=lambda d: d.offset)
        for n in range(len(sorted_drains)-1):
            d1 = sorted_drains[n]
            d2 = sorted_drains[n+1]

            if d1.offset >= self.get_source().offset and d1.offset < self.get_sink().offset \
               and d2.offset > self.get_source().offset and d2.offset <= self.get_sink().offset:
            
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
                             fill=fill,
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

                dwg.add(p)


    def center_at(self, x):
        for d in self.drains:
            d.x = x

class Drain(Base):
    __tablename__ = 'drains'
    id = Column(Integer, primary_key=True)
    x = Column(Float, default=0)
    width = Column(Float, default=0)
    offset = Column(Float, default=0)

    # artificial drains are automatically created to match courses
    artificial = Column(Boolean, default=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship(lambda:Course,
                          back_populates="drains")

    def __repr__(self):
        if self.artificial:
            a = '<'
        else:
            a = '['
        return "%s o=%s x=%s w=%s [%s]" % (a, self.offset, self.x, self.width, self.id)


class River():
    def __init__(self, courses=[], init=True):
        # auto init courses
        if init:
            self.courses = session.query(
                Course).order_by(Course.id.desc()).all()
        else:
            self.courses = courses

    def match_shores(self):
        """ update x on all drains """
        longest = self.get_longest_course()
        longest.center_at(self.get_max_width()*0.5)
        
        courses = sorted(self.courses,
                         key=lambda c: c.length,
                         reverse=True)
        
        for i in range(1, len(courses)):
            left = courses[i - 1]
            right = courses[i]
            for j in range(len(left.drains)):
                right.drains[j].x = left.drains[j].x \
                                    + left.drains[j].width * 0.5 \
                                    + right.drains[j].width * 0.5

                print left.drains[j], right.drains[j]
                

            
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
                if d not in c.drains:
                    c.add_drain(Drain(offset=d.offset,
                                      width=c.get_width_at_offset(d.offset),
                                      artificial=True))

    def get_max_width(self):
        self.match_drains()

        widths = {}
        for d in session.query(
                Drain).order_by(Drain.offset).all():
            if d.offset in widths:
                widths[d.offset] += d.width
            else:
                widths[d.offset] = d.width

        return sorted(widths.values())[-1]

    def get_longest_course(self):
        return sorted(self.courses,
                      key=lambda c: c.length)[-1]
        
    def flow_together(self):
        pass
        # longest.center_at(self.get_max_width()*0.5)
        
        # alternating in decreasing order
        # flank left
        # flank right



# on assembling the river:
# longest course should be centered
# flank it with decreasing order length
# horizontal center everything querying max width of river





from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

nile = Course(label='nile',
              drains=[Drain(offset=1, width=40),
                      Drain(offset=50, width=60),
                      Drain(offset=150, width=80)])

session.add(nile)
session.commit()

volga = Course(label='volga',
           drains=[Drain(offset=30, width=10),
                   Drain(offset=70, width=20),
                   Drain(offset=100, width=30)])
session.add(volga)
session.commit()


river = River()
river.match_drains()
river.match_shores()

dwg = svgwrite.Drawing(filename='prueba.svg')
nile.svg_paths(dwg, 'purple')
volga.svg_paths(dwg, 'navy')
dwg.save()
