import flask
from flask import request, Response
import pandas as pd
import json


app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods = ['GET'])
def home():
    return '<h1>Welcome to add numbers</h1>'

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if (request.method == 'GET'):
        try:
            num1 = 0
            num2 = 0
            if ('num1' in request.args):
                num1 = int(request.args['num1'])
            if ('num2' in request.args):
                num2 = int(request.args['num2'])
            result = str(num1 + num2)
            return Response(result, status=200)
        except:
            return Response(status=400)
            
    if (request.method == 'POST'):
        try:
            json_request = json.loads(request.data)
            data2 = pd.DataFrame(json_request)
            data2['result'] = data2.num1 + data2.num2
            return Response(data2.to_json(), status=200)
        except:
            return Response(status=400)
app.run()
