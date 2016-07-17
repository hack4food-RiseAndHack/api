import random
import string
import json

from flask_restful import Resource
from flask import request


class OpenTransaction(Resource):
    transactionStore = None
    completeStore = None
    sessionStore = None

    def __init__(self, transactionStore, completeStore, sessionStore):
        self.transactionStore = transactionStore
        self.completeStore = completeStore
        self.sessionStore = sessionStore

    def post(self):
        token = request.args.get("token")
        username = self.sessionStore.get(token)
        if username is None:
            return {"success": False, "message": "Unauthorized"}, 401

        reqData = request.get_json()

        if reqData is None or "price" not in reqData or "accountNumber" not in reqData:
            return {"success": False, "message": "Incorrect transaction"}

        reqData["username"] = username

        uid = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
        self.transactionStore.setex(name=uid, value=json.dumps(reqData), time=30)
        return {"success": True, "uid": uid}
