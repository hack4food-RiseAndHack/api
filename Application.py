from flask import Flask
from flask_restful import Resource, Api
import redis

from Resources.OpenTransaction import OpenTransaction
from Resources.Session import Session
from Resources.Registration import Registration
from Resources.TransactionManage import TransactionManage
from Domain.TransactionValidator import TransactionValidator
from Domain.RegistrationVerification import RegistrationVerification


app = Flask("API")
api = Api(app)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

redisTransactionStore = redis.StrictRedis(db=0)
redisUserStore = redis.StrictRedis(db=1)
redisSessionStore = redis.StrictRedis(db=2)

registerVerification = RegistrationVerification(redisUserStore)

api.add_resource(Registration, "/register",
                 resource_class_kwargs={"redis": redisUserStore, "verification": registerVerification})
api.add_resource(OpenTransaction, '/open',
                 resource_class_kwargs={"redis": redisTransactionStore})
api.add_resource(Session, '/session',
                 resource_class_kwargs={"userStore": redisUserStore, "sessionStore": redisSessionStore})
api.add_resource(TransactionManage, '/transaction/<uid>',
                 resource_class_kwargs={"sessionStore": redisSessionStore, "transactionStore": redisTransactionStore})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
