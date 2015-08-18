from backend import app
from flask import jsonify,request
from parser import Message, User, Chat, Statistics
from cStringIO import StringIO

@app.route('/api/uploadChat',methods=['POST'])
def upload_chat():
	chat = Chat(StringIO(request.files['file'].read()))
	users = [u.name for u in chat.users]
	stats_chat = Statistics(chat)
	charts = {'charts':[stats_chat.return_messages_by_user(as_chart=True),stats_chat.return_share_of_messages_by_user(as_chart=True)]}
	return jsonify(charts)
