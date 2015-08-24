import os
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

app = Flask('groupstats',static_url_path='',static_folder=os.getcwd()+'/frontend/dist')
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

from backend import upload