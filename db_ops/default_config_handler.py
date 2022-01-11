import sys

from .mongo_db_doc import MongoDBDoc

sys.path.append("..")

from env_vars import DEFAULT_CHANNEL


class DefaultConfigHandler(MongoDBDoc):
    """
    [
        {
            "_id": "default_config",
            "channel_id": int(123),
            "auto_schedule": True,
        }
    ]
    """

    def __init__(self):
        super().__init__(_collection="server_configs", _doc_name="default_config")

    def set_init_config(self):
        self.channel_id = DEFAULT_CHANNEL
        if self.auto_schedule is None:
            self.auto_schedule = True

    """
    channel_id
    """

    def __get_channel_id(self):
        return self.db_get_value_by_key("channel_id")

    def __set_channel_id(self, channel_id):
        self.db_upsert_field_value("channel_id", channel_id)

    def __del_channel_id(self):
        self.db_delete_field("channel_id")

    """
    auto_schedule
    """

    def __get_auto_schedule(self):
        return self.db_get_value_by_key("auto_schedule")

    def __set_auto_schedule(self, auto_schedule):
        self.db_upsert_field_value("auto_schedule", auto_schedule)

    def __del_auto_schedule(self):
        self.db_delete_field("auto_schedule")

    """
    Properties
    """
    channel_id = property(__get_channel_id, __set_channel_id, __del_channel_id)
    auto_schedule = property(__get_auto_schedule, __set_auto_schedule, __del_auto_schedule)
