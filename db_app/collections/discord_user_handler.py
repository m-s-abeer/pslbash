from db_app.mongo_data_classes.mongo_db_doc import MongoDBDoc
from db_app.mongo_data_classes.pymongo_singleton import fsdb

db = fsdb.get_fsdb()


class DiscordUserHandler(MongoDBDoc):
    """
    [
        {
            "_id": int(discord_id),
            "uuid": int(discord_id),
            "disabled": bool()
        }
    ]
    """

    def __init__(self, _discord_id):
        super().__init__(_collection="discord_users", _doc_name=_discord_id)
        self.uuid = _discord_id
        if self.disabled is None:
            self.disabled = False

    @staticmethod
    def get_all_user_id_list():
        all_discord_user_id_list = [int(id) for id in db["discord_users"].find().distinct("_id") if isinstance(id, int)]
        return all_discord_user_id_list

    """
    uuid
    """

    def get_uuid(self):
        return self.db_get_value_by_key("uuid")

    def set_uuid(self, uuid):
        self.db_upsert_field_value("uuid", uuid)

    def del_uuid(self):
        self.db_delete_field("uuid")

    uuid = property(get_uuid, set_uuid, del_uuid)

    """
    mention
    """

    @property
    def mention(self):
        return f"<@!{self.uuid}>"

    """
    disabled
    """

    def get_disabled(self):
        return self.db_get_value_by_key("disabled")

    def set_disabled(self, disabled):
        self.db_upsert_field_value("disabled", disabled)

    def del_disabled(self):
        self.db_delete_field("disabled")

    disabled = property(get_disabled, set_disabled, del_disabled)
