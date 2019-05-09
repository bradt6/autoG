from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import settings

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_photo_table(engine):
    DeclarativeBase.metadata.create_all(engine)


def create_Tag_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Photos(DeclarativeBase):

    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    tags = relationship("Tags")


class Tags(DeclarativeBase):

    __tablename__ = "tags"

    id = Column(Integer, primary_key = True)
    tag = Column('tag', String)
    photos_id = Column('photos_id', Integer, ForeignKey('photos.id'))







    
