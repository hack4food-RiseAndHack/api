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
            return Session.error(), 401

        userData = json.loads(userQuery)
        token = None
        try:
            if reqData["password"] == userData["password"]:
                token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
                self.sessionStore.setex(name=token, value=userData["username"], time=300)
            else:
                return Session.error(), 401
        except TypeError:
            return Session.error(), 401

        return {"success": True, "message": "You have logged in", "token": token}

    def get(self):
        token = request.args.get("token")
        if token is None:
            return {"success": False, "message": "Not logged in"}

        sessionData = self.sessionStore.get(token)
        if sessionData is None:
            return {"success": False, "message": "Not logged in"}

        self.sessionStore.setex(name=token, value=sessionData, time=300)
        return {"success": True, "message": "You are logged in", "username": sessionData}

    def delete(self):
        token = request.args.get("token")
        if token is None:
            return {"success": False, "message": "You have to provide a token"}

        self.sessionStore.delete(token)
        return {"success": True, "message": "Logged out"}
