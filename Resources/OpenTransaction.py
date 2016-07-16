from flask_restful import Resource


class OpenTransaction(Resource):
    redis = None

    def post(self):
        return
