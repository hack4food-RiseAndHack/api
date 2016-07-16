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

        (success, message) = self.verification.verify(json)
        if not success:
            return {"success": False, "message": message}

        self.redis.set(name=json["username"], value=json)
        return {"success": True}
