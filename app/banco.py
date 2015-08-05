from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Contact, Institution, TagName, Tag
from flask.ext.heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

engine = create_engine(os.environ["DATABASE_URL"])
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts/save', methods=['POST'])
def saveContact():

    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            print key,":",value

    phone1 = request.form['phone1']
    phone2 = request.form['phone2']
    address = request.form['address']
    notes = request.form['notes']
    lat = request.form['lat']
    lng = request.form['lng']

    #point_of_contact = Contact(institution=test_inst1, latitude=lat, longitude=lng, address=address, telephone1=phone1, telephone2=phone2, notas=notes)
    #session.add(point_of_contact)
    #session.commit()

    return "success"


@app.route('/home')
def home():
    if request.method == 'GET':
        items = session.query(TagName).all()
        tags=[i.serialize for i in items]
        return render_template('home.html', tags=tags)

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