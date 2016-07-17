from flask_restful import Resource
from flask import request


class TransactionVerification(Resource):
    sessionStore = None
    transactionStore = None
    completeStore = None

    def __init__(self, sessionStore, transactionStore, completeStore):
        self.sessionStore = sessionStore
        self.transactionStore = transactionStore
        self.completeStore = completeStore

    def put(self, uid):
        token = request.args.get("token")
        if token is None:
            return {"success": False, "message": "You must provide a token"}, 401
        username = self.sessionStore.get(token)

        decision = request.get_data()
        if decision == "DENY":
            self.transactionStore.delete(uid)
            return {"success": False, "message": "Transaction canceled"}

        complete = self.transactionStore.get(uid)
        self.completeStore.rpush(username, complete)
