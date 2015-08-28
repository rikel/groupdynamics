from backend import app, db
from flask import jsonify,request
from parser import Message, User, Chat, Statistics
from cStringIO import StringIO
from models import Record
import json
import datetime
import os
import uuid

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
	else:
   		ip = request.remote_addr
	record['ip_addr'] = ip
	record['url_id'] = str(uuid.uuid4())
	parent_url = request.form['url_id']
	if parent_url:
		parent = Record.query.filter_by(url_id = parent_url).first()
		if parent:
			record['parent_id'] = parent.id

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
	record['chart_config_json'] = json.dumps(charts)
	record = Record(**record)
	db.session.add(record)
	db.session.commit()
	return jsonify({
		'url_id':record.url_id, 
		'number_of_messages':charts['number_of_messages'], 
		'number_of_users':charts['number_of_users']
		})

@app.route('/api/getconfig',methods=['POST'])
def get_config():
	url_id  = request.json['url_id']
	record = Record.query.filter_by(url_id=url_id).first()
	return record.chart_config_json

def get_file_size(fileobj):
	fileobj.seek(0,os.SEEK_END)
	return fileobj.tell()