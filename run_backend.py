#!venv/bin/python
from flask.ext.script import Manager
from backend import app,db
from flask.ext.migrate import Migrate, MigrateCommand

app.host = '0.0.0.0'
app.debug = False

migrate= Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

@manager.command
def runapp(debug=True):
    if debug:
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'
    return app.run(debug=debug,host=host,port=8080)

#app.run(debug=True)
if __name__ == "__main__":
    db.create_all()
    manager.run()