from flask_restful import Resource
from flask import request
import json


class Registration(Resource):
    redis = None
    verification = None

    def __init__(self, redis, verification):
        self.redis = redis
        self.verification = verification

    def post(self):
        reqData = request.get_json()

        (success, message) = self.verification.verify(reqData)
        if not success:
            return {"success": False, "message": message}

        jDump = json.dumps(reqData)
        self.redis.set(name=reqData["username"], value=jDump)
        return {"success": True}
