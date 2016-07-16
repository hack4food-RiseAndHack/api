class RegistrationVerification(object):
    redis = None

    def __init__(self, redis):
        self.redis = redis

    def verify(self, json):
        if self.redis.get(json["username"]) is not None:
            return False
        return True
