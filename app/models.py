from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


job_location = Table(
    "job_location",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("location_id", ForeignKey("locations.id"), primary_key=True),
)

job_skill = Table(
    "job_skill",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id"), primary_key=True),
)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    
    jobs = relationship("Job", secondary=job_location, back_populates="locations")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    
    jobs = relationship("Job", secondary=job_skill, back_populates="skills")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    salary = Column(Integer)
    remote = Column(Boolean, default=False)

    
    locations = relationship("Location", secondary=job_location, back_populates="jobs")
    skills = relationship("Skill", secondary=job_skill, back_populates="jobs")
