#!venv/bin/python
from backend import app

app.host = '0.0.0.0'
app.debug = False

#app.run(debug=True)
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)