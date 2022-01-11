import sys
from pymongo import MongoClient
sys.path.append("..")

from env_vars import MONGO_CERT_PATH

class SingletonDB:
    _fsdb = None

    def __init__(self, *args, **kwargs):
        if not self._fsdb:
            uri = "mongodb+srv://pslbash.t89vp.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
            client = MongoClient(
                uri, tls=True, tlsCertificateKeyFile=MONGO_CERT_PATH
            )

            self._fsdb = client["pslbash"]

    def get_fsdb(self):
        return self._fsdb


fsdb = SingletonDB()
