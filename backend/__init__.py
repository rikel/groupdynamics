import os
from flask import Flask, jsonify, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

app = Flask('groupstats',static_url_path='',static_folder=os.getcwd()+'/frontend/app')
app.config.update(
	SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
)
#app.config['STATIC'] = 'frontend/app'

#create db object
db = SQLAlchemy(app)
db.create_all()

@app.route('/api/test',methods=['GET'])
def test_route():
	return jsonify({'message':'Hello, world!'})

@app.route('/')
def send_index():
	return app.send_static_file('index.html')

@app.route('/bower_components/<path:filename>')
def send_bower_components(filename):
	return send_from_directory(os.getcwd()+'/frontend/bower_components/',filename)

from backend import upload