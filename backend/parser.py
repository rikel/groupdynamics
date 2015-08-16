import numpy as np
import random
import cStringIO


class Message(object):

	def __init__(self, id_message, id_user, text, media_text="Media omitted"):
		self.id = id_message
		self.text = text
		self.isMedia = media_text in text
		self.id_user = id_user



class User(object):

	def __init__(self, id_user, name_user):
		self.id_user = id_user
		self.name = name_user
		self.messages = dict()
		self.num_messages = 0
		self.num_media = 0

	def read_messages(self, list_messages):
		for elt in list_messages:
			self.messages[elt[0]] = elt[1]
		self.num_messages = len(self.messages)

	def read_media(self, text="Media omitted"):
		self.media = []
		for k, v in self.messages.iteritems():
			if text in v:
				self.media.append(k)
		self.num_media = len(self.media)

	def display_info(self):
		print "----------------------"
		print "User {}: {}. Number of Messages: {}.".format(self.id_user, self.name, self.num_messages)
		print "Total Length of Messages: {}.".format(np.sum([len(v) for v in self.messages.values()]))

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
				if name not in chat:
					chat[name] = []
				chat[name].append((i, l))

		for k, v in chat.iteritems():
			if len(v) >= self.min_num_mess:
				self.users.append(User(len(self.users), k))
				self.users[-1].read_messages(v)
				chat_def[k] = [elt[0] for elt in v]

		self.chat = chat_def




# example of main code
if __name__ == "__main__":
	filename = "GOB.txt"
	p = Chat(filename)

	for u in p.users:
	    u.display_info()
	    u.read_media()
	    print u.get_random_message()
	    print "# Media = {}, # Mess = {}, Ratio = {}.".format(u.num_media, u.num_messages, float(u.num_media) / u.num_messages)


