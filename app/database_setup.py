import os
import sys
from flask import Flask
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
from flask.ext.heroku import Heroku
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, UserMixin

 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SECRET_KEY'] = 'super-secret'
db = SQLAlchemy(app)
engine = create_engine(os.environ["DATABASE_URL"])

class Institution(db.Model):
    __tablename__ = 'institutions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(250))
    telephone1 = Column(String(15))
    telephone2 = Column(String(15))
    email = Column(String(255))
    url = Column(String(512))
    description = Column(String(2000))

    @property
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "address" : self.address,
            "phone1" : self.telephone1,
            "phone2" : self.telephone2,
            "email" : self.email,
            "url" : self.url,
            "description" : self.description
        }

class Contact(db.Model):
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
    tags = relationship("Tag", cascade="all, delete-orphan", backref="contacts")

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


class TagName(db.Model):
    __tablename__ = 'tag_names'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    @property
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name
        }


class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id', ondelete='CASCADE'))
    contact = relationship("Contact", foreign_keys=[contact_id])
    tag_name_id = Column(Integer, ForeignKey('tag_names.id'))
    tag_name = relationship("TagName", foreign_keys=[tag_name_id])



class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean)
    inst_id = Column(Integer, ForeignKey('institutions.id'))
    institution = relationship(Institution)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship(Role)

    def get(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)



engine = create_engine(os.environ["DATABASE_URL"])
db.create_all()
