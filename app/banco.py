from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Contact, Institution, TagName, Tag
from flask.ext.heroku import Heroku
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    UserMixin,
    RoleMixin,
    login_required)
from flask_security.utils import encrypt_password
import os


app = Flask(__name__)
heroku = Heroku(app)

engine = create_engine(os.environ["DATABASE_URL"])
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        usr = request.form['user']
        passwd = request.form['passwd']
        print usr
        print passwd
        return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return ('hola mundo')    

@app.route('/contacts/save', methods=['POST'])
def saveContact():
    print request.form
    phone1 = request.form['phone1']
    phone2 = request.form['phone2']
    address = request.form['address']
    notes = request.form['notes']
    lat = request.form['lat']
    lng = request.form['lng']

    point_of_contact = Contact(institution=test_inst1, latitude=lat, longitude=lng, address=address, telephone1=phone1, telephone2=phone2, notas=notes)
    session.add(point_of_contact)
    session.commit()

    return "success"

@app.route('/home')
def home():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/search')
def search():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    rad = request.args.get('radius')

    if not lat or not lng:
        return

    magicQuery = text(
        """SELECT * FROM
            (SELECT c.id, c.latitude AS lat, c.longitude AS lng, c.address, c.notas, i.name, i.address AS hq, i.description, i.telephone1, i.telephone2, i.email, i.url, 
                    (6371 * acos(cos(radians(:lat)) * cos(radians(c.latitude)) * cos(radians(c.longitude) - radians(:lng)) + sin(radians(:lat)) * sin(radians(c.latitude)))) AS distance 
             FROM contacts AS c INNER JOIN institutions AS i
             ON c.inst_id = i.id) AS t1
        WHERE distance < :r """)

    items = session.execute(magicQuery, {"lat":lat, "lng":lng, "r":rad})
    
    resultset = []
    for row in items:
        resultset.append(dict(row))

    res = jsonify(items=resultset)
    return res

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)