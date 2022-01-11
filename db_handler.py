from db_ops.default_config_handler import DefaultConfigHandler
from db_ops.discord_user_handler import DiscordUserHandler
from user_data_repo import UserData
from utils import get_cur_bangladeshi_date, get_cur_bangladeshi_time
import discord

client = discord.Client()


# def get_keys(obj):
#     try:
#         keys = [str(key) for key in dict(obj).keys()]
#         return keys
#     except:
#         return []


# def set_last_holiday_message_sent(cur_date):
#     cur_date = str(cur_date)
#     db['config']['last_holiday_message_sent'] = cur_date


# def get_last_holiday_message_sent():
#     if ('last_holiday_message_sent' not in db['config'].keys()):
#         db['config']['last_holiday_message_sent'] = "None"
#     return db['config']['last_holiday_message_sent']


def get_is_schedule_active():
    return DefaultConfigHandler().auto_schedule


def get_is_active(user_data):
    return not user_data.disabled


# async def remove_profile_with_id(user_id):
#     user_id = str(user_id)
#     if user_id in db['id_profiles'].keys():
#         del db['id_profiles'][user_id]


async def get_all_user_data():
    user_id_list = DiscordUserHandler.get_all_user_id_list()
    return [UserData(user_id) for user_id in user_id_list]


def get_broadcast_channel():
    return DefaultConfigHandler().channel_id


def get_last_checked_in(user_data):
    return user_data.last_checkin


async def set_last_checked_in(user_data):
    user_data.last_checkin = (str(get_cur_bangladeshi_date()), str(get_cur_bangladeshi_time()))


async def clear_last_checked_in(user_data):
    user_data.last_checkin = ("", "")


def get_last_checked_out(user_data):
    return user_data.last_checkout


async def set_last_checked_out(user_data):
    user_data.last_checkout = (str(get_cur_bangladeshi_date()), str(get_cur_bangladeshi_time()))


async def clear_last_checked_out(user_data):
    user_data.last_checkout = ("", "")
