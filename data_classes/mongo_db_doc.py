from .pymongo_singleton import fsdb

db = fsdb.get_fsdb()


class MongoDBDoc:
    def __init__(self, _collection, _doc_name):
        self.collection = db[_collection]
        self.doc_name = _doc_name

    def __get_doc_obj(self):
        doc_obj = self.collection.find_one({"_id": self.doc_name})
        return doc_obj

    def db_get_value_by_key(self, key):
        try:
            doc = self.__get_doc_obj()
            ret_val = doc[key]
        except:
            ret_val = None

        return ret_val

    def db_upsert_field_value(self, field_name, value):
        self.collection.update_one({"_id": self.doc_name}, {"$set": {field_name: value}}, upsert=True)

    def db_delete_field(self, key):
        self.collection.update_one({"_id": self.doc_name}, {"$unset": {key: None}})
