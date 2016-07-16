class TransactionValidator(object):
    pass

    def verify(self, json):
        if json is not None and "price" in json:
            return False
        return True
