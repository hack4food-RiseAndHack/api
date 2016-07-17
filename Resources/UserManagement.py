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

        newData = json.loads(request.get_json())
        del newData["username"]

        if "password" not in newData or "email" not in newData:
            return {"success": False, "message": "new Password and/or email must be present"}, 400

        newBlob = json.dump(newData)
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
