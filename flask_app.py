
# Evaluation project for a certain company
from flask import Flask
from flask import request
from flask import jsonify
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

# Per documentation, it is recommended to have one MongoDB connection for writes,
# and another one for reads
mongo_write = pymongo.MongoClient('mongodb://{}:{}@ds135624.mlab.com:35624/techeval'
                            .format(app.config['MONGO_USERNAME'],
                                    app.config['MONGO_PASSWORD']))
mongo_read = pymongo.MongoClient('mongodb://{}:{}@ds135624.mlab.com:35624/techeval'
                                 .format(app.config['MONGO_USERNAME'],
                                    app.config['MONGO_PASSWORD']))
write_db = mongo_write.get_database()
read_db = mongo_read.get_database()

# Create all the indexes that we are going to need
write_db.transactions.create_index([("tuid", pymongo.DESCENDING), ("timestamp", pymongo.ASCENDING)])
write_db.transactions.create_index([("ref_tuid", pymongo.DESCENDING), ("timestamp", pymongo.ASCENDING)])
write_db.transactions.create_index([("source", pymongo.DESCENDING), ("tuid", pymongo.DESCENDING)])
write_db.transactions.create_index([("destination", pymongo.DESCENDING), ("tuid", pymongo.DESCENDING)])

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def hello_world():
    return 'Welcome to the Evaluation Project ;)'

def clean_results(x):
    """
    The results returned by MongoDB will have the _id attribute in each object. This
    function removes it, as it is not needed in the result given to the user.
    """
    del(x['_id'])
    return x

@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        data = request.get_json()
        try:
            in_id = write_db.transactions.insert_one(data).inserted_id
            return 'POST is successful on /history with id={}'.format(in_id)
        except:
            return 'POST failed on /history!', 500
    elif request.method == 'GET':
        tuid = request.args.get('tuid', None)
        wuid = request.args.get('wuid', None)
        if tuid:
            cur = read_db.transactions.find({'$or': [{"tuid": tuid}, {"ref_tuid": tuid}]}).sort("timestamp", pymongo.ASCENDING)
            results = [clean_results(x) for x in cur]
            return jsonify(results)
        if wuid:
            cur = read_db.transactions.find({'$or': [{"source": wuid}, {"destination": wuid}]}).sort("tuid", pymongo.DESCENDING)
            tmpresults = [clean_results(x) for x in cur]
            # In tmpresults, transactions with the same tuid will be next to each other.
            if tmpresults:
                results = [[tmpresults[0]]]
                for i in range(1, len(tmpresults)):
                    if results[-1][0]["tuid"] == tmpresults[i]["tuid"]:
                        results[-1].append(tmpresults[i])
                    else:
                        results[-1].sort(key=lambda x: x["timestamp"]) # sort the list with same tuids, before adding a new tuid list
                        results.append([tmpresults[i]])
                results[-1].sort(key=lambda x: x["timestamp"]) # Sorting the final element that was left unsorted when the loop ended
                results = sorted(results, key=lambda x: x[0]["timestamp"], reverse=True) # Sorting the outer loop by timestamp
            else:
                results = []
            return jsonify(results)
        if tuid and wuid:
            raise(InvalidUsage(message='Invalid input. Time for tea.', status_code=418))
        return 'GET received on /history!'


