from backend import app, db

class Record(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	ip_addr = db.Column(db.String)
	file_size = db.Column(db.Float)
	number_of_messages = db.Column(db.Integer)
	number_of_users = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime)
	url_id = db.Column(db.String,unique=True)
	parent_id = db.Column(db.Integer,db.ForeignKey(id))

	children = db.relationship("Record", 
		cascade="save-update, merge, refresh-expire, expunge",
		backref=db.backref("parent", remote_side=id))


	chart_config_json = db.Column(db.Text) 

	def __init__(self,**kwargs):
		for key,value in kwargs.items():
			castKey = getattr(Record,key).expression.type.__repr__()
			setattr(self,key,value)