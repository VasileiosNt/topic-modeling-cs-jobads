from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, DateTime, Float, Boolean, Text
from scrapy.utils.project import get_project_settings


Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class MonsterJob(Base):
    __tablename__ = "Monster"

    id = Column(Integer, primary_key="True")
    JobId = Column(String)
    Title = Column(String)
    Location = Column(String)
    Company = Column(String)
    Description = Column(Text())
    Country = Column(String)
