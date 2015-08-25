import numpy as np
import random
from dateutil.parser import parse
import time
import datetime
from collections import defaultdict
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
		self.num_emoticons = 0

	def read_messages(self, list_messages):
		for elt in list_messages:
			self.messages.append(Message(elt[0], self.id_user, elt[1], elt[2]))
		self.num_messages = len(self.messages)
		self.read_media()
		self.count_emoticons()

	def read_media(self, text="Media omitted"):
		self.media = [m.id_message for m in self.messages if m.isMedia]
		self.num_media = len(self.media)

	def count_emoticons(self):
		self.num_emoticons = np.sum([m.text.encode('ascii', 'xmlcharrefreplace').count("&#") for m in self.messages])

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
				if ":" not in s[1]:
					continue
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

	def user_for_message(self, id_message):
		for u in self.users:
			if id_message in [m.id_message for m in u.messages]:
				return u
		return -1

	def return_username(self, id_user):
		for u in self.users:
			if u.id_user == id_user:
				return u.name
		return -1

	def display_summary(self):
		print "Summary of Chat -------------"
		total_num_messages = np.sum([u.num_messages for u in self.users])
		total_chars_messages = np.sum([np.sum([len(m.text) for m in u.messages]) for u in self.users])
		print "# of Users: {}. Total # of Messages: {}. Average Length Message: {}.".format(len(self.users), total_num_messages, total_chars_messages / float(total_num_messages))
		print "Max # messages per user: {}. Min # messages per user: {}.".format(max([u.num_messages for u in self.users]), min([u.num_messages for u in self.users]))

	def return_total_messages(self):
		return np.sum([u.num_messages for u in self.users])

	def return_total_users(self):
		return len(self.users)

class Statistics(object):

	def __init__(self, chat):
		self.chat = chat
		user_names = {u.id_user:u.name for u in self.chat.users}
		list_messages = [{'time':from_timestamp_to_date(m.date), 'id_message':m.id_message, 'isMedia':m.isMedia, 'user_id':m.id_user, 'user_name':user_names[m.id_user]} for u in self.chat.users for m in u.messages]
		self.df = pd.DataFrame(list_messages).set_index('time')

	def return_number_messages(self):
		return { u.name:u.num_messages for u in self.chat.users }

	def return_number_media(self):
		return { u.name:u.num_media for u in self.chat.users }

	def return_ratio_messages_media(self):
		return { u.name:float(u.num_media) / u.num_messages for u in self.chat.users }

	def return_conversations(self, thr_min=30):

		seconds_min = 60
		dist_conversation = thr_min * seconds_min
		conversations, message_to_conv = [], dict()
		conv_to_messages, conv_to_users = defaultdict(list), defaultdict(list)

		messages_time = self.df[['id_message']]

		tstamp_message = zip([int(val * 1E-9) for val in messages_time.index.values.tolist()], messages_time.values[:,0])
		tstamp_message = sorted(tstamp_message, key=lambda elt: elt[0])

		num_conv = -1
		last_date = - 2 * dist_conversation
		for elt in tstamp_message:
			if elt[0] - last_date >= dist_conversation:
				num_conv += 1
			message_to_conv[elt[1]] = num_conv
			last_date = elt[0]

		for k, v in message_to_conv.iteritems():
			conv_to_messages[v].append(k)
			conv_to_users[v].append(self.chat.user_for_message(k))

		return conv_to_messages, conv_to_users

	def compute_graph_conversations(self, conv_to_messages, conv_to_users):

		graph, user_counts = dict(), defaultdict(int)

		for u1 in self.chat.users:
			for u2 in self.chat.users:
				if u1.id_user < u2.id_user:
					graph[(u1.id_user, u2.id_user)] = 0

		for c in conv_to_users.values():
			set_users = list(set(c))
			for u1 in set_users:
				user_counts[u1.id_user] += 1
				for u2 in set_users:
					if u1.id_user >= u2.id_user:
						continue
					graph[(u1.id_user, u2.id_user)] += 1

		for id1, id2 in graph.keys():
			graph[(id1, id2)] /= max(user_counts[id1], user_counts[id1])

		return graph

	def return_messages_by_user(self, as_chart=False):

		m_by_user = self.df[['user_name', 'id_message']].groupby('user_name').count()
		m_by_user['Number of Messages'] = m_by_user['id_message']
		m_by_user = m_by_user[['Number of Messages']].sort(['Number of Messages'], ascending=[0])

		if as_chart:
			config = serialize(m_by_user, kind='bar', title='Number of Messages',
							   output_type='json', rot=45)

			config["yAxis"][0]["labels"]["rotation"] = 0
			config["xAxis"]["title"]["text"] = "user"
			config["yAxis"][0]["title"] = {"text": "# messages"}
			config["chart"]["marginTop"] = 70
			return {'options':config, 'series':config['series']}
		else:
			return m_by_user

	def return_share_of_messages_by_user(self, as_chart=False):

		share_by_user = self.df[['user_name','id_message']].groupby('user_name').count()
		total_num_messages = share_by_user['id_message'].sum()
		share_by_user['Share of Messages'] = 100.0 * share_by_user['id_message'] / total_num_messages
		share_by_user = share_by_user[['Share of Messages']]

		if as_chart:
			tooltip = {'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'}
			config = serialize(share_by_user, kind='pie', title='Share of Messages',
							   output_type='json', tooltip=tooltip)
			config["chart"]["marginTop"] = 70
			return {'options':config, 'series':config['series']}
		else:
			return share_by_user


	def return_emoticons_by_user(self, as_chart=False):

		e_by_user = pd.DataFrame({u.name:u.num_emoticons for u in self.chat.users}.items(), columns=['user', 'Number of Emoticons'])
		e_by_user = e_by_user.sort(['Number of Emoticons'], ascending=[1])
		e_by_user.set_index('user', inplace=True)

		if as_chart:
			config = serialize(e_by_user, kind='bar', title='Number of Emoticons',
							   output_type='json', rot=45)

			config["xAxis"]["title"]["text"] = "user"
			config["yAxis"][0]["labels"]["rotation"] = 0
			config["yAxis"][0]["title"] = {"text": "# emoticons"}
			config["chart"]["marginTop"] = 70
			return {'options':config, 'series':config['series']}
		else:
			return e_by_user

	def return_ratio_media_messages_by_user(self, as_chart=False):

		media_by_user = self.df[self.df.isMedia == True][['user_name', 'isMedia']].groupby('user_name').count()
		message_by_user = self.df[['user_name', 'id_message']].groupby('user_name').count()
		message_by_user['Number of Media'] = media_by_user['isMedia']
		message_by_user.fillna(0, inplace=True)

		message_by_user['Percentage of Photo/Video Messages'] = 100.0 * message_by_user['Number of Media'] / message_by_user['id_message']
		message_by_user = message_by_user[['Percentage of Photo/Video Messages']].sort(['Percentage of Photo/Video Messages'], ascending=[0])
		message_by_user = np.round(message_by_user, decimals=2)

		if as_chart:
			tooltip = {'pointFormat': '{series.name}: <b>{point.y}%</b>'}
			config = serialize(message_by_user, kind='barh', title='Percentage of Photo/Video Messages',
							   output_type='json', tooltip=tooltip)

			config["xAxis"]["title"]["text"] = "user"
			config["yAxis"][0]["title"] = {"text": "percentage of media messages"}
			config["chart"]["marginTop"] = 70
			return {'options':config, 'series':config['series']}
		else:
			return message_by_user

	def return_number_of_messages_by_hour(self, as_chart=False):

		m_by_hour = self.df[['id_message']].copy()
		m_by_hour.loc[:, 'hour'] = m_by_hour.index.hour
		m_by_hour = m_by_hour.groupby('hour').count()
		
		if as_chart:
			config = serialize(m_by_hour, kind='line', title='Number of Messages per Hour of the Day',
							   output_type='json')

			config["yAxis"][0]["title"] = {"text": "# messages"}
			config["series"][0]["name"] = "Number of Messages"
			config["chart"]["marginTop"] = 70
			return {'options':config, 'series':config['series']}
		else:
			return m_by_hour

	def return_number_of_messages_by_hour_and_user(self, as_chart=False):

		m_by_hour_user = self.df[['id_message','user_name']].copy()
		m_by_hour_user.loc[:, 'hour'] = m_by_hour_user.index.hour
		m_by_hour_user = m_by_hour_user.groupby(['hour','user_name']).count().unstack().fillna(0)

		names_to_show = []
		for elt in m_by_hour_user.columns:
		    names_to_show.append(elt[1])
		m_by_hour_user.columns = names_to_show

		if as_chart:
			config = serialize(m_by_hour_user, kind='bar', title='Number of Messages by Hour and User',
							   output_type='json')

			config["yAxis"][0]["title"] = {"text": "# messages"}
			config["chart"]["marginTop"] = 70

			for k, v in config.iteritems():
				if k == "series":
					r = np.random.choice(len(v), 2, replace=False)
					for j, d in enumerate(v):
						if j not in r:
							config["series"][j]["visible"] = False

			return {'options':config, 'series':config['series']}
		else:
			return m_by_hour_user

	def return_number_of_messages_by_week_and_year(self, as_chart=False):

		m_by_week_year = self.df[['id_message']].copy()
		m_by_week_year.loc[:, 'year'] = m_by_week_year.index.year
		m_by_week_year.loc[:, 'week'] = m_by_week_year.index.week
		m_by_week_year = m_by_week_year.groupby(['year', 'week']).count()

		if as_chart:
			config = serialize(m_by_week_year, kind='bar', title='Total Number of Messages by Week and Year',
							   output_type='json', rot=45)
			config["yAxis"][0]["labels"]["rotation"] = 0
			config["series"][0]["name"] = "Number of Messages"
			config["yAxis"][0]["title"] = {"text": "# messages"}
			config["chart"]["marginTop"] = 70
			return {'options':config, 'series':config['series']}
		else:
			return m_by_week_year



# example of main code
if __name__ == "__main__":
	filename = "GOB.txt"
	p = Chat(filename)

	for u in p.users:
	    u.display_info()
	    u.read_media()
	    print u.get_random_message()
	    print "# Media = {}, # Mess = {}, Ratio = {}.".format(u.num_media, u.num_messages, float(u.num_media) / u.num_messages)
