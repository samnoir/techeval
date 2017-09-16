
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from flask import jsonify


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

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/history', methods=['GET', 'POST'])
def history():
    print(request.method)
    if request.method == 'POST':
        return 'POST is successful on /history!'
    elif request.method == 'GET':
        tuid = request.args.get('tuid', None)
        wuid = request.args.get('wuid', None)
        if tuid:
            print('TUID=', tuid)
        if wuid:
            print('WUID=', wuid)
        if tuid and wuid:
            raise(InvalidUsage(message='What am I? A teapot?', status_code=418))
        return 'GET received on /history!'
    

    