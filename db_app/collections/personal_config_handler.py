from db_app.mongo_data_classes.mongo_db_doc import MongoDBDoc


class PersonalConfigHandler(MongoDBDoc):
    """
    [
        {
            "_id": int(discord_id),
            "vacation": bool(),
            "checkin_after": {
                "hh": int(),
                "mm": int()
            },
            "checkout_after": {
                "hh": int(),
                "mm": int()
            }
        }
    ]
    """

    def __init__(self, _discord_id):
        super().__init__(_collection="personal_configs", _doc_name=_discord_id)
        if self.vacation is None:
            self.vacation = False

    """
    vacation
    """

    def __get_vacation(self):
        return self.db_get_value_by_key("vacation")

    def __set_vacation(self, vacation):
        self.db_upsert_field_value("vacation", vacation)

    def __del_vacation(self):
        self.db_delete_field("vacation")

    vacation = property(__get_vacation, __set_vacation, __del_vacation)

    """
    checkin_after
    """

    def __get_checkin_after(self):
        return self.db_get_value_by_key("checkin_after")

    def __set_checkin_after(self, checkin_after):
        hh, mm = checkin_after
        self.db_upsert_field_value("checkin_after", {"hh": hh, "mm": mm})

    def __del_checkin_after(self):
        self.db_delete_field("checkin_after")

    checkin_after = property(__get_checkin_after, __set_checkin_after, __del_checkin_after)

    """
    checkout_after
    """

    def __get_checkout_after(self):
        return self.db_get_value_by_key("checkout_after")

    def __set_checkout_after(self, checkout_after):
        hh, mm = checkout_after
        self.db_upsert_field_value("checkout_after", {"hh": hh, "mm": mm})

    def __del_checkout_after(self):
        self.db_delete_field("checkout_after")

    checkout_after = property(__get_checkout_after, __set_checkout_after, __del_checkout_after)
