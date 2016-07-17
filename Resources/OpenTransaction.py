import random
import string
import json

from flask_restful import Resource
from flask import request


class OpenTransaction(Resource):
    redis = None
    verification = None

    def __init__(self, redis):
        self.redis = redis

    def post(self):
        reqData = request.get_json()

        if reqData is not None and "price" not in reqData:
            return {"success": False, "message": "Incorrect transaction"}

        uid = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
        self.redis.setex(name=uid, value=json.dumps(reqData), time=300)
        return {"success": True, "uid": uid}
