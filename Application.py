from flask import Flask
from flask_restful import Resource, Api
import redis

from Resources.OpenTransaction import OpenTransaction
from Resources.Session import Session
from Resources.Registration import Registration
from Domain.TransactionValidator import TransactionValidator
from Domain.RegistrationVerification import RegistrationVerification


app = Flask("API")
api = Api(app)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

redisTransactionStore = redis.StrictRedis(db=0)
redisUserStore = redis.StrictRedis(db=1)

registerVerification = RegistrationVerification(redisUserStore)

api.add_resource(Registration, "/register",
                 resource_class_kwargs={"redis": redisUserStore, "verification": registerVerification})
api.add_resource(OpenTransaction, '/open',
                 resource_class_kwargs={"redis": redisTransactionStore})
api.add_resource(Session, '/session')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
