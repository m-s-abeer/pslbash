from pymongo import MongoClient


class SingletonDB:
    _fsdb = None

    def __init__(self, *args, **kwargs):
        if not self._fsdb:
            uri = "mongodb+srv://pslbash.t89vp.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
            client = MongoClient(
                uri, tls=True, tlsCertificateKeyFile="/home/msabeer/dev/pslbash/db_ops/mongo_db_cert.pem"
            )

            self._fsdb = client["pslbash"]

    def get_fsdb(self):
        return self._fsdb


fsdb = SingletonDB()
