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
        return session.query(Drain).with_parent(self, 'course').order_by(User.id).first()

    # last drain
    def sink(self):
        # add not-artificial to query        
        return session.query(Drain).with_parent(self, 'course').order_by(User.id).desc().first()
    
    def update_length(self):
        if session.query(Drain).with_parent(self, 'course').order_by(User.id).count()>=2:
            self.length = self.source().offset - self.sink.offset
            


    def add_drain(self, drain):
        self.drains.append(drain)
        self.update_length()


    
class Drain(Base):
    __tablename__ = 'drains'
    id       = Column(Integer, primary_key=True)    
    width = Column(Float)
    offset = Column(Float)

    artificial = Column(Boolean)
    course_id  = Column(Integer, ForeignKey('courses.id'))
    course     = relationship("Course",
                              back_populates="drains")



# on assembling the river:
# longest course should be centered
# flank it with decreasing order length
# horizontal center everything querying max width of river
#class River(Base):
#    pass
    



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

