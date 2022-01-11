from .mongo_db_doc import MongoDBDoc
from .pymongo_db_config import fsdb

db = fsdb.get_fsdb()


class DiscordUserHandler(MongoDBDoc):
    """
    [
        {
            "_id": int(discord_id),
            "uuid": int(discord_id),
            "uuid": str(discord_mention),
            "disabled": bool()
        }
    ]
    """

    def __init__(self, _discord_id, mention_string=None):
        super().__init__(_collection="discord_users", _doc_name=_discord_id)
        self.uuid = _discord_id
        if self.disabled is None:
            self.disabled = False
        if mention_string and self.mention != mention_string:
            self.mention = mention_string

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

    def get_mention(self):
        return self.db_get_value_by_key("mention")

    def set_mention(self, mention):
        self.db_upsert_field_value("mention", mention)

    def del_mention(self):
        self.db_delete_field("mention")

    mention = property(get_mention, set_mention, del_mention)

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
