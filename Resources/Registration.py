from flask_restful import Resource
from flask import request


class Registration(Resource):
    redis = None
    verification = None

    def __init__(self, redis, verification):
        self.redis = redis
        self.verification = verification

    def post(self):
        json = request.get_json()

        if not self.verification.verify(json):
            return {"success": False, "message": "Invalid user data"}

        self.redis.set(name=json["username"], value=json)sele
        return {"success": True}
