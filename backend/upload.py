from backend import app, db
from flask import jsonify,request
from parser import Message, User, Chat, Statistics
from cStringIO import StringIO
from models import Record
import datetime
import os

@app.route('/api/uploadChat',methods=['POST'])
def upload_chat():
	strio = StringIO(request.files['file'].read())
	chat = Chat(strio)
	record = {}
	record['file_size'] = get_file_size(strio)
	record['number_of_messages'] = chat.return_total_messages()
	record['number_of_users'] = chat.return_total_users()
	record['timestamp'] = datetime.datetime.now()
	if request.headers.getlist("X-Forwarded-For"):
   		ip = request.headers.getlist("X-Forwarded-For")[0]
   		print ip
	else:
   		ip = request.remote_addr
   		print ip
   	print ip
	record['ip_addr'] = ip
	record = Record(**record)
	db.session.add(record)
	db.session.commit()
	users = [u.name for u in chat.users]
	stats_chat = Statistics(chat)
	charts = {
		'charts':[stats_chat.return_messages_by_user(as_chart=True),
				  stats_chat.return_share_of_messages_by_user(as_chart=True),
				  stats_chat.return_ratio_media_messages_by_user(as_chart=True),
				  stats_chat.return_number_of_messages_by_hour(as_chart=True),
				  stats_chat.return_number_of_messages_by_hour_and_user(as_chart=True),
				  stats_chat.return_emoticons_by_user(as_chart=True),
				  stats_chat.return_number_of_messages_by_week_and_year(as_chart=True)],
		'number_of_messages':chat.return_total_messages(),
		'number_of_users':chat.return_total_users()
			}
	return jsonify(charts)


def get_file_size(fileobj):
	fileobj.seek(0,os.SEEK_END)
	return fileobj.tell()