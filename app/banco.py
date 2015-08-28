from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from database_setup import Contact, Institution, TagName, Tag, User
from flask.ext.heroku import Heroku
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    UserMixin,
    RoleMixin,
    login_required)
from flask_security.utils import encrypt_password
import os
import bcrypt
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, UserMixin
from flask.ext.mail import Mail, Message
from config import ADMINS
import random
import string
from functools import wraps
import sqlalchemy.exc
import sqlalchemy

app = Flask(__name__)
heroku = Heroku(app)
mail = Mail(app)

engine = create_engine(os.environ["DATABASE_URL"])

DBSession = sessionmaker(bind=engine)
session = DBSession()

app.config['SECRET_KEY'] = 'randomHashoSecretKey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(id):
    return User.get(id)

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def get_current_user_role():
    if(current_user.is_authenticated()):
        return str(current_user.role_id)

def error_response():
    return "unathorized"

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

def validatePassword(usuario, passwd):
    user =  User.query.filter_by(email=usuario).first()
    if(user):
        if(bcrypt.hashpw(passwd, user.password.encode('utf-8')) == user.password):
            login_user(user)
            return True
        else:
            return False   


def redirectUser():
    if current_user.role_id == 2:
        return redirect('/home')
    else:
        return redirect('/registro')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated():
            return redirectUser()
        else:
            return render_template('login.html')
    else:
        passwd = request.form['passwd'].encode('utf-8')
    if(validatePassword(request.form['user'],passwd)):
        return redirectUser()
    else:
        return render_template('login.html', error="email o contrasena incorrectos")
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def resetPassword():
   user = User.query.filter_by(email=request.form['user']).first()
   if(user):
    user.password = generateRandomPassword()
    print user.password
    session.commit()


def generateRandomPassword():
    s=string.lowercase+string.digits
    passwd = ''.join(random.sample(s,10))
    passwd.encode('utf-8')
    print passwd
    hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
    return hashed

@app.route("/forgot",methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        resetPassword()
        #send_email('asunto','tsu_carlosescamilla@hotmail.com','cescamilla@ooyala.com','mensaje body','<b>HTML</b> body')
        return render_template('forgot.html',feedback = "Email enviado")  
    else:
        return render_template('forgot.html')  

@app.route('/')
def index():
    items = session.query(TagName).all()
    tags=[i.serialize for i in items]       
    return render_template('index.html', tags=tags)


@app.route('/registro',methods=['GET'])
@login_required
@requires_roles('1')
def registerOrganization():
    Organizations = session.query(Institution).all()
    return render_template('registerOrganization.html',organizations=Organizations)



@app.route("/registro/save",methods=['POST'])
@login_required
@requires_roles('1')
def saveOrganization():
    print 'puto beto'
    f = request.form
    print f
    phone1 = f['phone1']
    phone2 = f['phone2']
    address1 = f['address']
    email = f['email']
    url = f['url']
    name = f['name']
    passwd = f['passwd'].encode('utf-8')
    hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
    descripcion = f['descripcion']
    organization = Institution(name=name,telephone1=phone1,telephone2=phone2,description=descripcion,url=url,email=email, address=address1) 
    usuario = User(email=email,password=hashed,institution=organization,role_id = 2,active=True)
    try:
        session.add(organization)
        session.add(usuario)
        session.commit()
    except sqlalchemy.exc.IntegrityError, exc:
        reason = exc.message
        session.rollback()
        if('users_email_key' in reason):
                return "El email ya esta registrado, por favor intente nuevamente con otro email"

    return 'success'






@app.route('/contacts/save', methods=['POST'])
def saveContact():
    f = request.form
    inst = current_user.inst_id
    institution = session.query(Institution).filter(Institution.id == inst).first()

    phone1 = f['phone1']
    phone2 = f['phone2']
    address = f['address']
    notes = f['notes']
    lat = f['lat']
    lng = f['lng']
    email = f['email']
    name = f['name']
    url = f['url']

    point_of_contact = Contact(institution=institution, name=name, latitude=lat, longitude=lng, address=address, 
        telephone1=phone1, telephone2=phone2, notas=notes, url=url, email=email)

    session.add(point_of_contact)
    session.commit()

    for i in f.getlist('tag'):
        tag_name = session.query(TagName).filter(TagName.id == i).first()
        tag = Tag(contact = point_of_contact, tag_name=tag_name)
        session.add(tag)
        session.commit()
    
    return "success"



@app.route("/institutions",methods=['GET'])
@login_required
def getOrganizationsJSON():
    institutions = session.query(Institution).all()
    return jsonify(items=[i.serialize for i in institutions])    


@app.route('/contacts')
def getContacts():
    inst = current_user.inst_id
    institution = session.query(Institution).filter(Institution.id == inst).first()
    contacts = session.query(Contact).filter(Contact.institution == institution).all()
    return jsonify(items=[i.serialize for i in contacts])


@app.route('/home')
@login_required
def home():
    if request.method == 'GET':
        items = session.query(TagName).all()
        tags=[i.serialize for i in items]

        inst = current_user.inst_id

        institution = session.query(Institution).filter(Institution.id == inst).first()
        contacts = session.query(Contact).filter(Contact.institution == institution).all()
        serialized_contacts = [i.serialize for i in contacts]

        return render_template('home.html', tags=tags, contacts=serialized_contacts)


@app.route('/search')
def search():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    rad = request.args.get('radius')

    if not lat or not lng:
        return

    #magicQuery = text(
    #    """SELECT * FROM
    #        (SELECT c.id, c.latitude AS lat, c.longitude AS lng, c.address, c.notas, c.name AS c_name, i.name, i.address AS hq, i.description, i.telephone1, i.telephone2, i.email, i.url, 
    #                (6371 * acos(cos(radians(:lat)) * cos(radians(c.latitude)) * cos(radians(c.longitude) - radians(:lng)) + sin(radians(:lat)) * sin(radians(c.latitude)))) AS distance 
    #         FROM contacts AS c INNER JOIN institutions AS i
    #         ON c.inst_id = i.id) AS t1
    #    WHERE distance < :r """)

    magicQuery = text(
        """SELECT * FROM
            (SELECT c.id, c.latitude AS lat, c.longitude AS lng, c.address, c.notas, c.name AS c_name, i.name, i.address AS hq, i.description, i.telephone1, i.telephone2, i.email, i.url,
                    (6371 * acos(cos(radians(:lat)) * cos(radians(c.latitude)) * cos(radians(c.longitude) - radians(:lng)) + sin(radians(:lat)) * sin(radians(c.latitude)))) AS distance 
            FROM contacts AS c 
            INNER JOIN institutions AS i
            ON c.inst_id = i.id
            ) AS t1
        WHERE distance < :r """)

    items = session.execute(magicQuery, {"lat":lat, "lng":lng, "r":rad})
    
    resultset = []
    for row in items:
        d = dict(row)
        #Adding tags for each contact
        tags_rows = session.execute(text("SELECT * FROM tags INNER JOIN tag_names on (tags.tag_name_id = tag_names.id) WHERE tags.contact_id =:contact_id"), {"contact_id": d['id']})
        d['tags'] = [dict(i) for i in tags_rows]

        resultset.append(d)


    res = jsonify(items=resultset)
    return res

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)