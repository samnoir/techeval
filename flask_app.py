
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/history', methods=['GET', 'POST'])
def history():
    print(request.method)
    if request.method == 'POST':
        return 'POST is successful on /history!'
    elif request.method == 'GET':
        return 'GET received on /history!'