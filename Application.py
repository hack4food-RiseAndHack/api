from flask import Flask
from flask_restful import Resource, Api
import redis

from Resources.OpenTransaction import OpenTransaction
from Resources.Session import Session
from Domain.TransactionValidator import TransactionValidator


app = Flask("API")
api = Api(app)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

redisConnection = redis.StrictRedis()
api.add_resource(OpenTransaction, '/open',
                 resource_class_kwargs={"redis": redisConnection})
api.add_resource(Session, '/session')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
