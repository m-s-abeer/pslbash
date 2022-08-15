from db_app.collections.discord_user_handler import DiscordUserHandler
from db_app.collections.ho_credential_handler import HoCredentialHandler
from db_app.collections.personal_config_handler import PersonalConfigHandler
from db_app.collections.attendance_log_handler import AttendanceLogHandler


class UserData:
    def __init__(self, discord_id):
        self.discord_user = DiscordUserHandler(discord_id)
        self.ho_credential = HoCredentialHandler(discord_id)
        self.personal_config = PersonalConfigHandler(discord_id)
        self.attendance_log = AttendanceLogHandler(discord_id)

    @property
    def uuid(self):
        return self.discord_user.uuid

    @uuid.setter
    def uuid(self, uuid):
        self.discord_user.uuid = uuid

    @property
    def mention(self):
        return self.discord_user.mention

    @property
    def disabled(self):
        return self.discord_user.disabled

    @disabled.setter
    def disabled(self, disabled):
        self.discord_user.disabled = disabled

    @property
    def email(self):
        return self.ho_credential.ho_email

    @email.setter
    def email(self, email):
        self.ho_credential.ho_email = email

    @property
    def password(self):
        return self.ho_credential.ho_pass

    @password.setter
    def password(self, password):
        self.ho_credential.ho_pass = password

    @property
    def vacation(self):
        return self.personal_config.vacation

    @vacation.setter
    def vacation(self, vacation):
        self.personal_config.vacation = vacation

    @property
    def checkin_after(self):
        return self.personal_config.checkin_after

    @checkin_after.setter
    def checkin_after(self, checkin_after):
        self.personal_config.checkin_after = checkin_after

    @property
    def checkout_after(self):
        return self.personal_config.checkout_after

    @checkout_after.setter
    def checkout_after(self, checkout_after):
        self.personal_config.checkout_after = checkout_after

    @property
    def last_checkin(self):
        return self.attendance_log.last_checkin

    @last_checkin.setter
    def last_checkin(self, last_checkin):
        self.attendance_log.last_checkin = last_checkin

    @property
    def last_checkout(self):
        return self.attendance_log.last_checkout

    @last_checkout.setter
    def last_checkout(self, last_checkout):
        self.attendance_log.last_checkout = last_checkout
