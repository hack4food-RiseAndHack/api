from flask import Flask
from flask_restful import Resource, Api

from Resources.OpenTransaction import OpenTransaction
from Resources.Session import Session

app = Flask(__name__)
api = Api(app)

api.add_resource(OpenTransaction, '/open')
api.add_resource(Session, '/session')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
