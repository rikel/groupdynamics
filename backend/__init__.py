import os
from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object('config')

@app.route('/api/test',methods=['GET'])
def test_route():
	return jsonify({'message':'Hello, world!'})