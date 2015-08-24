from app import app, db

class Upload(BaseModel,db.Model):
	'''
	This class defines the different fund deals and their relevant information.
	Importantly, it links funds to their fund functions.
	'''
	#--- Begin Raw Data---
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String,nullable=False)
	npvFunction = db.Column(db.String,nullable=False)
	tranches = db.relationship('Tranche',backref='fund')
	fmvs = db.relationship('FMVDeal',backref='fund')
	def __init__(self,**kwargs):
		for key,value in kwargs.items():
			castKey = getattr(Fund,key).expression.type.__repr__()
			setattr(self,key,castDict[castKey](value))

	def computeNPV(self,fund,fmvByState={}):
		function = npvFunctions[self.npvFunction](fmvByState)
		return function(fund)