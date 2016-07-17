from flask_restful import Resource
from flask import request
import json


class UserManagement(Resource):
    sessionStore = None
    userStore = None

    def __init__(self, sessionStore, userStore):
        self.userStore = userStore
        self.sessionStore = sessionStore

    def post(self):
        token = request.args.get('token')
        if token is None:
            return {"success": False, "message": "You must provide a token"}, 401

        username = self.sessionStore.get(token)
        if username is None:
            return {"success": False, "message": "Session expired"}, 401

        oldData = json.loads(self.userStore.get(username))
        newData = request.get_json()
        
        username = oldData["username"]

        for key, value in newData.iteritems():
            oldData[key] = value

        oldData["username"] = username
        newBlob = json.dumps(oldData)
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
