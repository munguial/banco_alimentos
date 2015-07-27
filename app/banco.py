from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Contact, Institution, TagName, Tag

app = Flask(__name__)


engine = create_engine('postgresql://amunguia:@localhost/banco')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    items = session.query(Institution).all()
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
    return render_template('index.html', chido = output)

@app.route('/search')
def search():
	lat = request.args.get('lat')
	lng = request.args.get('lng')
	rad = request.args.get('radius')

	if not lat or not lng:
		return

	magicQuery = text(
		"""SELECT * FROM
			(SELECT c.id, c.latitude AS lat, c.longitude AS lng, c.address, c.notas, i.name, i.address AS hq, i.description, 
			        (6371 * acos(cos(radians(:lat)) * cos(radians(c.latitude)) * cos(radians(c.longitude) - radians(:lng)) + sin(radians(:lat)) * sin(radians(c.latitude)))) AS distance 
			 FROM contacts AS c INNER JOIN institutions AS i
			 ON c.inst_id = i.id) AS t1
		WHERE distance < :r 
		ORDER BY distance 
		LIMIT 20""")

	items = session.execute(magicQuery, {"lat":lat, "lng":lng, "r":rad})
	
	resultset = []
	for row in items:
	    resultset.append(dict(row))

	res = jsonify(items=resultset)
	return res

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)