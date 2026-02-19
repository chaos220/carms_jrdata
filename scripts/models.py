from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Discipline(Base):
    __tablename__ = "discipline"
    id   = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class School(Base):
    __tablename__ = "school"
    id   = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) # , unique=True)

class Program(Base):
    __tablename__ = "program"
    id            = Column(Integer, primary_key=True)
    discipline_id = Column(Integer, ForeignKey("discipline.id"), nullable=False)
    school_id     = Column(Integer, ForeignKey("school.id"),     nullable=False)

    stream_id   = Column(Integer, nullable=False)
    stream_name = Column(String,  nullable=False)
    site        = Column(String,  nullable=False)
    name        = Column(String,  nullable=False)
    url         = Column(String,  nullable=False)
    raw_html    = Column(Text)

    # optional extracted columns – added later by a migration script
    quota          = Column(Integer)
    director_name  = Column(String)
    director_email = Column(String)
    interview_dates= Column(String)
    accreditation  = Column(String)

    discipline = relationship("Discipline")
    school     = relationship("School")

    __table_args__ = (UniqueConstraint('discipline_id',
                                      'school_id',
                                      'stream_id',
                                      name='uq_program_unique'),)