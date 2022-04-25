from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings



Base = declarative_base()

def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)

class IndeedJob(Base):
    __tablename__ = 'Indeed'
    
    id = Column(Integer,primary_key="True")
    
    JobId = Column(String)
    JobTitle= Column(String)
    Location = Column(String)
    Company = Column(String)
    Description = Column(Text())
    Rating = Column(String)
    Country = Column(String)
