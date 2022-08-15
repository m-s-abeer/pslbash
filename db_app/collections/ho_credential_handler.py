import sys

from db_app.mongo_data_classes.mongo_db_doc import MongoDBDoc

sys.path.append("../..")


class HoCredentialHandler(MongoDBDoc):
    """
    [
        {
            "_id": int(discord_id),
            "ho_email": "example@xyz.com",
            "ho_pass": "ho!ho!!ho!!!",
        }
    ]
    """

    def __init__(self, _discord_id):
        super().__init__(_collection="psl_ho_cred", _doc_name=_discord_id)

    """
    ho_email
    """

    def __get_ho_email(self):
        return self.db_get_value_by_key("ho_email")

    def __set_ho_email(self, email):
        self.db_upsert_field_value("ho_email", email)

    def __del_ho_email(self):
        self.db_delete_field("ho_email")

    ho_email = property(__get_ho_email, __set_ho_email, __del_ho_email)

    """
    ho_pass
    """

    def __get_ho_pass(self):
        return self.db_get_value_by_key("ho_pass")

    def __set_ho_pass(self, password):
        self.db_upsert_field_value("ho_pass", password)

    def __del_ho_pass(self):
        self.db_delete_field("ho_pass")

    ho_pass = property(__get_ho_pass, __set_ho_pass, __del_ho_pass)
