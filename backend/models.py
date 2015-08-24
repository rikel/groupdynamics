from backend import app, db

class Upload(db.Model):
	'''
	This class defines the different fund deals and their relevant information.
	Importantly, it links funds to their fund functions.
	'''
	#--- Begin Raw Data---
	id = db.Column(db.Integer,primary_key=True)
	ip_addr = db.Column(db.String)
	file_size = db.Column(db.Float)
	number_of_messages = db.Column(db.Integer)
	number_of_users = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime)

	def __init__(self,**kwargs):
		for key,value in kwargs.items():
			castKey = getattr(Fund,key).expression.type.__repr__()
			setattr(self,key,castDict[castKey](value))

	def computeNPV(self,fund,fmvByState={}):
		function = npvFunctions[self.npvFunction](fmvByState)
		return function(fund)