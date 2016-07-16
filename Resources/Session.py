import random
import string

from flask_restful import Resource
from flask import request
import json


class Session(Resource):
    userStore = None
    sessionStore = None

    def __init__(self, userStore, sessionStore):
        self.userStore = userStore
        self.sessionStore = sessionStore

    @staticmethod
    def error():
        return {"success": False, "message": "Invalid credentials"}

    def post(self):
        reqData = request.get_json()

        userData = self.userStore.get(reqData["username"])
        if userData is None:
            data = json.loads()
            if data is None:
                return Session.error()

        if reqData["password"] == data["password"]:
            token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
            self.sessionStore.setex(name=token, value=data["username"], time=30)

        return {"success": True, "message": "You have logged in", "token": token}
