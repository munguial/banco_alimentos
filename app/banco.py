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
    institution = session.query(Institution).filter(Institution.id == 1).first()

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


@app.route('/contacts')
def getContacts():
    institution = session.query(Institution).filter(Institution.id == 1).first()
    contacts = session.query(Contact).filter(Contact.institution == institution).all()
    return jsonify(items=[i.serialize for i in contacts])


@app.route('/home')
def home():
    if request.method == 'GET':
        items = session.query(TagName).all()
        tags=[i.serialize for i in items]

        institution = session.query(Institution).filter(Institution.id == 1).first()
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