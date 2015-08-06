
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from databaseSecurity import Contact, Institution, TagName, Tag
from flask.ext.heroku import Heroku
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    UserMixin,
    RoleMixin,
    login_required)
from flask_security.utils import encrypt_password
import os
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, UserMixin
from databaseSecurity import User
import bcrypt




app = Flask(__name__)
heroku = Heroku(app)

engine = create_engine(os.environ["DATABASE_URL"])
DBSession = sessionmaker(bind=engine)
session = DBSession()


app.config['SECRET_KEY'] = 'randomHashoneTwo'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        passwd = request.form['passwd'].encode('utf-8')
        user =  User.query.filter_by(email=request.form['user']).first()
    if (user):
        hashed = user.password.encode('utf-8')
        if(bcrypt.hashpw(passwd, hashed) == user.password):
            login_user(user)
            return redirect('/home')
        else:
            return render_template('login.html', error="email o contrasena incorrectos")
    else:
        return render_template('login.html', error="email o contrasena incorrectos")
         

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/demo')
@login_required
def demo():
    return ('hola mundo')    

@login_manager.user_loader
def load_user(id):
    return User.get(id)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@app.route('/registro')
def registerUser():
    institutions = Institution.query.all()
    return render_template('registerUser.html',dropdown=institutions)


@app.route('/home')
def home():
    if request.method == 'GET':
        return render_template('home.html')


if __name__ == '__main__':
    app.debug = True

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




