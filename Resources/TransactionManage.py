from flask_restful import Resource
from flask import request
import json


class TransactionManage(Resource):
    sessionStore = None
    transactionStore = None
    completeStore = None

    def __init__(self, sessionStore, transactionStore):
        self.sessionStore = sessionStore
        self.transactionStore = transactionStore

    def get(self, uid):
        token = request.args.get("token")
        if token is None:
            return {"success": False, "message": "You must provide a token"}, 401

        sessionData = self.sessionStore.get(token)


        if sessionData is None:
            return {"success": False, "message": "You are not logged in"}, 401

        transactionData = self.transactionStore.get(uid)
        if transactionData is None:
            return {"success": False, "message": "Transaction expired"}, 410

        return transactionData
