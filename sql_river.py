from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, \
    Boolean, create_engine, ForeignKey
from sqlalchemy.orm import relationship
import svgwrite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    label = Column(String(200), nullable=True)
    length = Column(Float, default=0)
    fill = Column(String(200), nullable=True)
    drains = relationship(lambda:Drain,
                          order_by=lambda: Drain.offset,
                          back_populates="course")


    def flank_with(self, other, side='right'):
        """ align another course to the edge of self """
        if side=='right':
            sign = 1
        elif side=='left':
            sign = -1

        for j in range(len(self.drains)):
            other.drains[j].x = self.drains[j].x \
                                + sign * self.drains[j].width * 0.5 \
                                + sign * other.drains[j].width * 0.5


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
        if offset <= self.get_source().offset \
           or offset >= self.get_sink().offset:
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

    def svg_paths(self, dwg):
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
            a = 'a'
        else:
            a = ' '
        return "<%s s%s %s@%s [%s]>" % (a, self.offset, self.width, self.x, self.id)


class River():
    def __init__(self, dwg, init=True):
        # auto init courses
        if init:
            self.courses = session.query(
                Course).order_by(Course.length.desc()).all()

        self.match_drains()
        self.center_align_all_courses()
        self.dwg = dwg

    def to_svg(self):
        for c in self.courses:
            c.svg_paths(self.dwg)

    def center_align_all_courses(self, margin=100):
        center = margin + self.get_max_width() * 0.5
        for c in self.courses:
            c.center_at(center)


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

    def get_rightmost_course(self):
        return session.query(Drain).order_by(Drain.x.desc()).first().course

    def get_leftmost_course(self):
        return session.query(Drain).order_by(Drain.x).first().course

    def get_max_width(self):

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

    def centralize_current(self):
        # iteration count for swinging between right and left
        n = 1
        # all but the longest course are outer courses
        for outer in sorted(self.courses,
                            key=lambda c: c.length, reverse=True)[1:]:
            if n % 2:
                side = 'left'
                inner = self.get_leftmost_course()
            else:
                side = 'right'
                inner = self.get_rightmost_course()
            inner.flank_with(outer, side)
            n+=1



engine = create_engine('sqlite:///:memory:', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
