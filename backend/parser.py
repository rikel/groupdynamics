import numpy as np
import random
from dateutil.parser import parse
import time
import datetime
import cStringIO
import pandas as pd
from pandas_highcharts.core import serialize

# constants
minute_hour = 60

# functions
def from_date_to_timestamp(date_string):
	try:
		dt = parse(date_string)
		return time.mktime(dt.timetuple())
	except:
		return -1

def from_timestamp_to_date(timestamp):
	return parse(time.strftime("%D %H:%M", time.localtime(int(timestamp))))

class Message(object):

	def __init__(self, id_message, id_user, date, text, media_text="Media omitted"):
		self.id_message = id_message
		self.date = date
		self.text = text
		self.isMedia = media_text in text
		self.id_user = id_user

	def display_message(self):
		print "Message Id = {}, Date = {}, From = {}".format(self.id_message, self.date, self.id_user)
		print "Text = {}.".format(self.text)
		print "isMedia? = {}.".format(self.isMedia)


class User(object):

	def __init__(self, id_user, name_user):
		self.id_user = id_user
		self.name = name_user
		self.messages = []
		self.num_messages = 0
		self.num_media = 0

	def read_messages(self, list_messages):
		for elt in list_messages:
			self.messages.append(Message(elt[0], self.id_user, elt[1], elt[2]))
		self.num_messages = len(self.messages)
		self.read_media()

	def read_media(self, text="Media omitted"):
		self.media = [m.id_message for m in self.messages if m.isMedia]
		self.num_media = len(self.media)

	def display_info(self):
		print "----------------------"
		print "User {}: {}. Number of Messages: {}.".format(self.id_user, self.name, self.num_messages)
		print "Total Length of Messages: {}.".format(np.sum([len(m.text) for m in self.messages]))

	def get_random_message(self):
		return self.messages.values()[random.randint(0, len(self.messages.values()))]


class Chat(object):

	def __init__(self, filename, min_num_mess=10):
		
		self.filename = filename
		self.min_num_mess = min_num_mess
		self.users = []

		self.read_file()
		self.parse_lines()

	def read_file(self):
		if type(self.filename) is str:
			with open(self.filename) as f:
				lines = f.readlines()
		elif isinstance(self.filename, cStringIO.InputType):
			lines = self.filename.readlines()
		self.lines = lines

	def parse_lines(self):

		chat, chat_def = dict(), dict()
		
		for i, l in enumerate(self.lines):
			s = l.split('-')
			if len(s) > 1:
				name = s[1].split(':')[0].lstrip()
				m_text = ":".join(s[1].split(':')[1:]).lstrip()
				if name not in chat:
					chat[name] = []
				date_message = from_date_to_timestamp(s[0].lstrip())
				chat[name].append((i, date_message, unicode(m_text, 'utf-8')))

		for k, v in chat.iteritems():
			if len(v) >= self.min_num_mess:
				self.users.append(User(len(self.users), k))
				self.users[-1].read_messages(v)
				chat_def[k] = [elt[0] for elt in v]

		self.chat = chat_def

	def display_summary(self):
		print "Summary of Chat -------------"
		total_num_messages = np.sum([u.num_messages for u in self.users])
		total_chars_messages = np.sum([np.sum([len(m.text) for m in u.messages]) for u in self.users])
		print "# of Users: {}. Total # of Messages: {}. Average Length Message: {}.".format(len(self.users), total_num_messages, total_chars_messages / float(total_num_messages))
		print "Max # messages per user: {}. Min # messages per user: {}.".format(max([u.num_messages for u in self.users]), min([u.num_messages for u in self.users]))


class Statistics(object):

	def __init__(self, chat):
		self.chat = chat
		user_names = {u.id_user:u.name for u in self.chat.users}

#		list_messages = [{'time':m.date, 'id_message':m.id_message, 'text':m.text, 'isMedia':m.isMedia, 'user_id':m.id_user, 'user_name':user_names[m.id_user]} for u in self.chat.users for m in u.messages]
		list_messages = [{'time':from_timestamp_to_date(m.date), 'id_message':m.id_message, 'isMedia':m.isMedia, 'user_id':m.id_user, 'user_name':user_names[m.id_user]} for u in self.chat.users for m in u.messages]


		self.df = pd.DataFrame(list_messages).set_index('time')


	def return_number_messages(self):
		return { u.name:u.num_messages for u in self.chat.users }

	def return_number_media(self):
		return { u.name:u.num_media for u in self.chat.users }

	def return_ratio_messages_media(self):
		return { u.name:float(u.num_media) / u.num_messages for u in self.chat.users }

	def return_time_curve(self):
		m_dates = []
		for u in self.chat.users:
			for m in u.messages:
				d = datetime.datetime.fromtimestamp(m.date)
				m_dates.append(d.hour * minute_hour + d.minute)
		return self.time_buckets(m_dates)

	def return_messages_by_user(self,as_chart=False):
		mByUser = self.df[['user_name','id_message']].groupby('user_name').aggregate(np.count_nonzero)
		mByUser['Number of Messages'] = mByUser['id_message']
		mByUser = mByUser[['Number of Messages']]
		if as_chart:
			config = serialize(mByUser,kind='bar',title='Number of Messages',output_type='json')
			return {'options':config,'series':config['series']}
		else:
			return mByUser

	def return_share_of_messages_by_user(self,as_chart=False):
		shareByUser = self.df[['user_name','id_message']].groupby('user_name').aggregate(np.count_nonzero)
		shareByUser['Share of Messages'] = shareByUser['id_message']*100.0/np.sum(shareByUser['id_message'])
		shareByUser = shareByUser[['Share of Messages']]
		if as_chart:
			tooltip = {'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'}
			config = serialize(shareByUser,kind='pie',title='Share of Messages',output_type='json',tooltip=tooltip)
			return {'options':config,'series':config['series']}
		else:
			return shareByUser

	def return_number_of_messages_by_hour(self,as_chart=False):
		byHour = self.df[['id_message']]
		byHour['hour'] = byHour.index.hour
		byHour = byHour.groupby('hour').aggregate(np.count_nonzero)
		if as_chart:
			config = serialize(byHour,kind='line',title='Number of Messages per Hour of the Day',output_type='json')
			return {'options':config,'series':config['series']}
		else:
			return byHour

	def return_number_of_messages_by_hour_and_user(self,as_chart=False):
		byHourAndUser = self.df[['id_message','user_name']]
		byHourAndUser['hour'] = byHourAndUser.index.hour
		byHourAndUser = byHourAndUser.groupby(['hour','user_name']).aggregate(np.count_nonzero).unstack().fillna(0)
		if as_chart:
			config = serialize(byHourAndUser,kind='bar',title='Number of Messages by Hour and User',output_type='json')
			return {'options':config,'series':config['series']}
		else:
			return byHourAndUser

	def time_buckets(self, messages_minutes, num_buckets=48):
    
		day_minutes = 24 * 60
		min_per_bucket = day_minutes / 48

		buckets = dict()

		for i in xrange(num_buckets):
			buckets[i] = 0
		for m in messages_minutes:
			b = int(np.floor(m / min_per_bucket))
			buckets[b] += 1

		return buckets



# example of main code
if __name__ == "__main__":
	filename = "GOB.txt"
	p = Chat(filename)

	for u in p.users:
	    u.display_info()
	    u.read_media()
	    print u.get_random_message()
	    print "# Media = {}, # Mess = {}, Ratio = {}.".format(u.num_media, u.num_messages, float(u.num_media) / u.num_messages)
