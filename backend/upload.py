from backend import app
from flask import jsonify,request
from parser import Message, User, Chat
from cStringIO import StringIO

@app.route('/api/uploadChat',methods=['POST'])
def upload_chat():
	chat = Chat(StringIO(request.files['file'].read()))
	users = [u.name for u in chat.users]
	return jsonify({'users':users})
