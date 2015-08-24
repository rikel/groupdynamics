#test again yet once more agaain!
import os
basedir = os.path.abspath(os.path.dirname(__file__))
URI = os.getenv('DB_ENDPOINT','')
if not URI:
	SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False')
else:
	SQLALCHEMY_DATABASE_URI = 'postgresql://groupstats:bowtieproject@'+os.environ['DB_ENDPOINT']+'/groupstats'