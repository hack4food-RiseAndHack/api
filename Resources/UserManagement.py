from flask_restful import Resource
from flask import request
import json


class UserManagement(Resource):
    sessionStore = None
    userStore = None

    def __init__(self, sessionStore, userStore):
        self.userStore = userStore
        self.sessionStore = sessionStore

    def post(self, username):
        token = request.args.get('token')

        if token is None:
            return {"success": False, "message": "You must provide a token"}, 401

        username = self.sessionStore.get(token)
        oldData = self.userStore.get(username)
        newData = json.loads(request.get_json())
        del newData["username"]

        for key, value in newData:
            if key in oldData:
                oldData[key] = value

        newBlob = json.dump(oldData)
        self.userStore.set(name=username, value=newBlob)
        return {"success": True, "message": "User updated"}

    def get(self):
        token = request.args.get("token")
        if token is None:
            return {"success": False, "message": "You must provide a token"}, 401

        username = self.sessionStore.get(token)
        if username is None:
            return {"success": False, "message": "Not authorized"}, 401

        userdata = json.loads(self.userStore.get(username))
        del userdata["password"]
        return userdata
