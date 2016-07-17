import time
import json

from flask_restful import Resource
from flask import request


class AwaitTransaction(Resource):
    transactionStore = None
    sessionStore = None
    completeStore = None

    def __init__(self, transactionStore, sessionStore, completeStore):
        self.transactionStore = transactionStore
        self.sessionStore = sessionStore
        self.completeStore = completeStore

    def get(self, uid):
        token = request.args.get("token")
        username = self.sessionStore.get(token)
        if username is None:
            return {"success": False, "message": "Not authorized"}, 401

        transactionBlob = self.transactionStore.get(uid)
        if transactionBlob is None:
            return {"success": False, "message": "Transaction expired"}

        transaction = json.loads(transactionBlob)
        if transaction is None or transaction["username"] != username:
            return {"success": False, "message": "Not authorized"}, 401

        start = time.time()
        expire = 40
        complete = False
        while not complete and time.time() < start + expire:
            transaction = self.transactionStore.get(uid)
            time.sleep(0.01)
            if transaction is not None and "complete" in transaction and transaction["complete"]:
                self.transactionStore.delete(uid)
                self.completeStore.rpush()
                return {"success": True, "message": "transaction completed"}
        return {"success": False, "message": "timed out"}