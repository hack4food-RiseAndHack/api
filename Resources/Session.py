from flask_restful import Resource


class Session(Resource):
    redis = None

    def post(self):
        return {"token": "12345456"}
