from flask_restful import Resource


class OpenTransaction(Resource):
    redis = None

    def __init__(self, redis):
        self.redis = redis

    def post(self):
        return
