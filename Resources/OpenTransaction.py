import random
import string

from flask_restful import Resource
from flask import request


class OpenTransaction(Resource):
    redis = None
    verification = None

    def __init__(self, redis):
        self.redis = redis

    def post(self):
        json = request.get_json()

        if json is not None and "price" not in json:
            return {"success": False, "message": "Incorrect transaction"}

        uid = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
        self.redis.setex(name=uid, value=str(json), time=30)
        return {"success": True, "uid": uid}
