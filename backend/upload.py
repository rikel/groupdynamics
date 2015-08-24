from backend import app
from flask import jsonify,request
from parser import Message, User, Chat, Statistics
from cStringIO import StringIO
from models import Upload

@app.route('/api/uploadChat',methods=['POST'])
def upload_chat():
	chat = Chat(StringIO(request.files['file'].read()))
	users = [u.name for u in chat.users]
	stats_chat = Statistics(chat)
	charts = {
		'charts':[stats_chat.return_messages_by_user(as_chart=True),
				  stats_chat.return_share_of_messages_by_user(as_chart=True),
				  stats_chat.return_number_of_messages_by_hour(as_chart=True),
				  stats_chat.return_number_of_messages_by_hour_and_user(as_chart=True),
				  stats_chat.return_number_of_messages_by_week_and_year(as_chart=True)],
		'number_of_messages':chat.return_total_messages(),
		'number_of_users':chat.return_total_users()
			}
	return jsonify(charts)
