#!/usr/bin/env python2.7

import redis
from flask import Flask
from flask_restful import Resource, Api
from Session import Session
from OpenTransaction import OpenTransaction

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


redisConnection = redis.StrictRedis(host="localhost", port=6379, db=0)

api.add_resource(HelloWorld, '/')
api.add_resource(OpenTransaction(redisConnection), "/open")
api.add_resource(Session(redisConnection), "/session")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
