from flask_restful import Resource


class Session(Resource):
    redis = None

    def __init__(self, redis):
        self.redis = redis

    def post(self):
        return {"token": "12345456"}
