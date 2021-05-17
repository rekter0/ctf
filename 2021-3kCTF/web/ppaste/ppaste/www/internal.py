from flask import Flask,request
import sqlite3
from contextlib import closing
import json

app = Flask(__name__)

def qDB(query,qtype='fetchAll',username=''):
    with closing(sqlite3.connect("/var/www/db/ppaste.db")) as connection:
        with closing(connection.cursor()) as cursor:
            if(qtype=='fetchAll'):
                rows = cursor.execute(query).fetchall()
                return rows
            elif(qtype=='setAdmin' and username!=''):
                cursor.execute(
					    query,
					    (username,)
					)
               	connection.commit()
                return 1
    return 0


@app.route('/invites', methods=['GET', 'POST'])
def invites():
    if request.method == 'POST':
        myJson = json.loads(request.data)
        if(myJson['invite'] in open('/var/www/invites.txt').read().split('\n')):
            return json.dumps(True)
        else:
            return json.dumps(False)
    return json.dumps(open('/var/www/invites.txt').read().split('\n'))


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        myJson = json.loads(request.data)
        if(myJson['user']):
        	qDB("UPDATE users SET priv=not(priv) WHERE user=? ","setAdmin",myJson['user'])
        	return json.dumps(True)
        else:
        	return json.dumps(False)
    return json.dumps(qDB("SELECT user,priv FROM users"))


@app.route('/')
def home():
    return 'internal console'


app.run(host='127.0.0.1', port=8082)


