from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, ForeignKey, Date, Text
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    id       = Column(Integer, primary_key=True)
    label    = Column(String(200), nullable=True)
    length = Column(Float, default=0)
    drains = relationship("Drain", back_populates="course")

    # first drain
    def source(self):
        # add not-artificial to query
        return session.query(Drain).with_parent(self).order_by(Drain.offset).first()

    # last drain
    def sink(self):
        # add not-artificial to query
        return session.query(Drain).with_parent(self).order_by(Drain.offset.desc()).first()

    def update_length(self):
        if session.query(Drain).with_parent(self).order_by(Drain.offset).count()>=2:
            self.length = self.sink().offset - self.source().offset

    def add_drain(self, drain):
        self.drains.append(drain)
        self.update_length()

    def __repr__(self):
        self.update_length()
        return "<course %s len=%s drains=%s>" % (self.label, self.length, len(self.drains))

    def get_max_width(self):
        return sorted(self.drains, key=lambda x: x.width, reverse=True)[0].width

    

class Drain(Base):
    __tablename__ = 'drains'
    id       = Column(Integer, primary_key=True)
    width = Column(Float, default=0)
    offset = Column(Float, default=0)

    # artificial drains are automatically created to match courses
    artificial = Column(Boolean, default=False)
    course_id  = Column(Integer, ForeignKey('courses.id'))
    course     = relationship("Course",
                              back_populates="drains")

    def __repr__(self):
        if self.artificial:
            a=' a'
        else:
            a=''
        return "<drain %s o=%s w=%s%s>" % (self.id, self.offset, self.width, a)



class River():
    def __init__(self, courses=[], init=True):
        
        # auto init courses
        if init:
            self.courses = session.query(Course).order_by(Course.id.desc()).all()
        else:
            self.courses=courses

        # match all drains
        all_drains = []
        for c in self.courses:
            all_drains += c.drains



    def get_width(self):
        w = 0
        for course in self.courses:
            w += course.get_max_width()
        return w
    
# on assembling the river:
# longest course should be centered
# flank it with decreasing order length
# horizontal center everything querying max width of river
#class River(Base):
#    pass




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

c=Course(label='volga',
         drains=[ Drain(offset=3, width=6),
                  Drain(offset=10, width=4)])
session.add(c)


c1=Course(label='nile',
         drains=[ Drain(offset=1, width=6),
                  Drain(offset=11, width=4),
                  Drain(offset=20, width=7)])

session.add(c1)
session.commit()

river = River()

