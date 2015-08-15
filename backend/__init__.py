import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/test',methods=['GET'])
def test_route():
	return jsonify({'message':'Hello, world!'})