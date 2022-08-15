from db_app.collections.default_config_handler import DefaultConfigHandler
from db_app.collections.discord_user_handler import DiscordUserHandler
from db_app.user_data_repo import UserData
from utils import get_cur_bangladeshi_date, get_cur_bangladeshi_time


async def get_all_user_data():
    user_id_list = DiscordUserHandler.get_all_user_id_list()
    return [UserData(user_id) for user_id in user_id_list]


def get_broadcast_channel():
    return DefaultConfigHandler().channel_id


async def set_last_checked_in(user_data):
    user_data.last_checkin = (str(get_cur_bangladeshi_date()), str(get_cur_bangladeshi_time()))


async def set_last_checked_out(user_data):
    user_data.last_checkout = (str(get_cur_bangladeshi_date()), str(get_cur_bangladeshi_time()))
