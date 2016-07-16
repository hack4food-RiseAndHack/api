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

        userQuery = self.userStore.get(reqData["username"])
        if userQuery is None:
            return Session.error()

        userData = json.loads(userQuery)

        try:
            if reqData["password"] == userData["password"]:
                token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
                self.sessionStore.setex(name=token, value=userData["username"], time=300)
        except TypeError:
            return Session.error()

        return {"success": True, "message": "You have logged in", "token": token}
