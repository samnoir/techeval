
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from flask import jsonify
#from flask_pymongo import PyMongo
#from flask_pymongo import ASCENDING, DESCENDING
import os
import sys
import pdb
import pymongo


class InvalidUsage(Exception):
    status_code = 400
    
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code:
            self.status_code = status_code
        self.payload = payload
        
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

app = Flask(__name__)
app.config['MONGO_HOST'] = 'ds135624.mlab.com'
app.config['MONGO_PORT'] = 35624
app.config['MONGO_DBNAME'] = 'techeval'
app.config['MONGO_USERNAME'] = os.environ.get('MONGO_USERNAME') or 'rouser'
app.config['MONGO_PASSWORD'] = os.environ.get('MONGO_PASSWORD') or 'ropw'

# mongodb://<dbuser>:<dbpassword>@ds135624.mlab.com:35624/techeval
#mongo = PyMongo(app)
mongo = pymongo.MongoClient('mongodb://currentuser:currentpw@ds135624.mlab.com:35624/techeval')
db = mongo.get_database()
#app.config['MONGO_READ_DBNAME'] = 'techeval'
#mongo_read = PyMongo(app, config_prefix='MONGO_READ') # Create a second Mongo object just for reads, to increase concurrency
db.transactions.create_index([("timestamp", pymongo.DESCENDING), ("tuid", pymongo.DESCENDING)])
db.transactions.create_index([("timestamp", pymongo.DESCENDING), ("ref_tuid", pymongo.DESCENDING)])

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def hello_world():
    #mongo.db.transactions.create_index([("timestamp", DESCENDING), ("tuid", DESCENDING)])
    #mongo.db.transactions.create_index([("timestamp", DESCENDING), ("ref_tuid", DESCENDING)])
    return 'Hello from Flask!'

def clean_results(x):
    del(x['_id'])
    return x

@app.route('/history', methods=['GET', 'POST'])
def history():
    print(request.method)
    if request.method == 'POST':
        data = request.get_json()
        try:
            in_id = db.transactions.insert_one(data).inserted_id
            return 'POST is successful on /history with id={}'.format(in_id)
        except:
            return 'POST is fail on /history!', 500
    elif request.method == 'GET':
        tuid = request.args.get('tuid', None)
        wuid = request.args.get('wuid', None)
        if tuid:
            print('GET with TUID=', tuid)
            cur = db.transactions.find({'$or': [{"tuid": tuid}, {"ref_tuid": tuid}]}).sort("timestamp", pymongo.DESCENDING)
            results = [clean_results(x) for x in cur]
            return jsonify(results)
        if wuid:
            print('WUID=', wuid)
            # Sort by tuid
        if tuid and wuid:
            raise(InvalidUsage(message='What am I? A teapot?', status_code=418))
        return 'GET received on /history!'
    

    