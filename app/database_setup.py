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
    name = Column(String(100), nullable=False)
    latitude = Column(Float(10,6), nullable=False)
    longitude = Column(Float(10,6), nullable=False)
    address = Column(String(250))
    telephone1 = Column(String(15))
    telephone2 = Column(String(15))
    email = Column(String(255))
    url = Column(String(512))
    notas = Column(String(2000))

    @property
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "lat" : str(self.latitude),
            "lng" : str(self.longitude),
            "address" : self.address,
            "phone1" : self.telephone1,
            "phone2" : self.telephone2,
            "email" : self.email,
            "url" : self.url,
            "notes" : self.notas
        }


class TagName(Base):
    __tablename__ = 'tag_names'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    @property
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name
        }


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship(Contact)
    tag_name_id = Column(Integer, ForeignKey('tag_names.id'))
    tag_name = relationship(TagName)


engine = create_engine(os.environ["DATABASE_URL"])
Base.metadata.create_all(engine)
