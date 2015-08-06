import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask.ext.sqlalchemy import SQLAlchemy
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    UserMixin,
    RoleMixin,
    login_required)
from flask_security.utils import encrypt_password
from flask import Flask

Base = declarative_base()
db = SQLAlchemy()
app = Flask(__name__)



class Institution(Base):
    __tablename__ = 'institutions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(250))
    telephone1 = Column(String(15))
    telephone2 = Column(String(15))
    email = Column(String(255))
    url = Column(String(512))
    description = Column(String(2000))

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    inst_id = Column(Integer, ForeignKey('institutions.id'))
    institution = relationship(Institution)
    latitude = Column(Float(10,6), nullable=False)
    longitude = Column(Float(10,6), nullable=False)
    address = Column(String(250))
    telephone1 = Column(String(15))
    telephone2 = Column(String(15))
    notas = Column(String(2000))

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