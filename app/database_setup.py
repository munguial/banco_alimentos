import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Institution(Base):
    __tablename__ = 'institutions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(250))
    description = Column(String(250))

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    inst_id = Column(Integer, ForeignKey('institutions.id'))
    institution = relationship(Institution)
    latitude = Column(Float(10,6), nullable=False)
    longitude = Column(Float(10,6), nullable=False)
    address = Column(String(250))
    notas = Column(String(500))

class TagName(Base):
    __tablename__ = 'tag_names'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship(Contact)
    tag_name_id = Column(Integer, ForeignKey('tag_names.id'))
    tag_name = relationship(TagName)


engine = create_engine(os.environ["DATABASE_URL"])
Base.metadata.create_all(engine)
