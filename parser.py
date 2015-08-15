import numpy as np

class User(object):

	def __init__(self, id_user, name_user):
		self.id = id_user
		self.name = name_user
		self.messages = dict()

	def read_messages(self, list_messages):
		for elt in list_messages:
			self.messages[elt[0]] = elt[1]


class Chat(object):

	def __init__(self, filename, min_num_mess=10):
		self.filename = filename
		self.min_num_mess = min_num_mess
		self.read_file()
		self.parse_lines()

	def read_file(self):
		with open(self.filename) as f:
			lines = f.readlines()
		self.lines = lines

	def parse_lines(self):
		chat, chat_def = dict(), dict()
		for i, l in enumerate(self.lines):
			s = l.split('-')
			if len(s) > 1:
				name = s[1].split(':')[0].lstrip()
				if name not in chat:
					chat[name] = []
				chat[name].append(i)

		for k, v in chat.iteritems():
			if len(v) >= self.min_num_mess:
				chat_def[k] = v

		self.chat = chat_def
