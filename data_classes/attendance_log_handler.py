from .mongo_db_doc import MongoDBDoc


class AttendanceLogHandler(MongoDBDoc):
    """
    [
        {
            "_id": int(discord_id),
            "last_checkin": {
                "date": "YYYY-MM-DD",
                "time": "HH:MM",
            },
            "last_checkout": {
                "date": "YYYY-MM-DD",
                "time": "HH:MM",
            },
        }
    ]
    """

    def __init__(self, _discord_id):
        super().__init__(_collection="attendance_log", _doc_name=_discord_id)
        if not self.last_checkin:
            self.last_checkin = ("0000-00-00", "00:00:00")
        if not self.last_checkout:
            self.last_checkout = ("0000-00-00", "00:00:00")

    """
    last_checkin
    """

    def __get_last_checkin(self):
        return self.db_get_value_by_key("last_checkin")

    def __set_last_checkin(self, last_checkin):
        date, time = last_checkin
        self.db_upsert_field_value("last_checkin", {"date": date, "time": time})

    def __del_last_checkin(self):
        self.db_delete_field("last_checkin")

    last_checkin = property(__get_last_checkin, __set_last_checkin, __del_last_checkin)

    """
    last_checkout
    """

    def __get_last_checkout(self):
        return self.db_get_value_by_key("last_checkout")

    def __set_last_checkout(self, last_checkout):
        date, time = last_checkout
        self.db_upsert_field_value("last_checkout", {"date": date, "time": time})

    def __del_last_checkout(self):
        self.db_delete_field("last_checkout")

    """
    Properties
    """
    last_checkout = property(__get_last_checkout, __set_last_checkout, __del_last_checkout)
