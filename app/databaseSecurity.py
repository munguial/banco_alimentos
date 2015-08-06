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


class Contact(db.Model):
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

class TagName(db.Model):
    __tablename__ = 'tag_names'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship(Contact)
    tag_name_id = Column(Integer, ForeignKey('tag_names.id'))
    tag_name = relationship(TagName)    

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

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
    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))
    inst_id = Column(Integer, ForeignKey('institutions.id'))
    institution = relationship(Institution)

    def get(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email


roles = db.relationship(
    'Role', secondary=roles_users,
    backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

