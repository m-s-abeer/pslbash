from replit import db
from utils import get_cur_bangladeshi_date, get_user_obj_with_id
import discord

client = discord.Client()


def get_keys(obj):
    try:
        keys = [str(key) for key in dict(obj).keys()]
        return keys
    except:
        return []


def set_last_holiday_message_sent(cur_date):
    cur_date = str(cur_date)
    db['config']['last_holiday_message_sent'] = cur_date


def get_last_holiday_message_sent():
    if ('last_holiday_message_sent' not in db['config'].keys()):
        db['config']['last_holiday_message_sent'] = "None"
    return db['config']['last_holiday_message_sent']


def get_is_schedule_active():
    if ('auto_schedule' not in db['config'].keys()):
        db['config']['auto_schedule'] = 1
    return int(db['config']['auto_schedule'])


def get_is_active(user):
    return int(db['id_profiles'][str(user.id)]['activated'])


async def remove_profile_with_id(user_id):
    user_id = str(user_id)
    if user_id in db['id_profiles'].keys():
        del db['id_profiles'][user_id]


async def get_all_users():
    user_id_list = get_keys(db['id_profiles'])
    user_list = []
    for user_id in user_id_list:
        user = await get_user_obj_with_id(user_id)
        if user:
            user_list.append(user)
    return user_list


def get_broadcast_channel():
    return db['config']['channel_id']


async def set_last_checked_in(user):
    db['id_profiles'][str(user.id)]['attendance']['last_checked_in'] = str(
        get_cur_bangladeshi_date())


async def clear_last_checked_in(user):
    db['id_profiles'][str(
        user.id)]['attendance']['last_checked_in'] = str('inf')


async def clear_last_checked_out(user):
    db['id_profiles'][str(
        user.id)]['attendance']['last_checked_out'] = str('inf')


async def set_last_checked_out(user):
    db['id_profiles'][str(user.id)]['attendance']['last_checked_out'] = str(
        get_cur_bangladeshi_date())


def get_email(user):
    if 'email' in db['id_profiles'][str(user.id)].keys():
        return db['id_profiles'][str(user.id)]['email']
    else:
        return ''


def get_last_checked_in(user):
    return db['id_profiles'][str(user.id)]['attendance']['last_checked_in']


def get_last_checked_out(user):
    return db['id_profiles'][str(user.id)]['attendance']['last_checked_out']


def set_attendance_format_if_missing(author):
    if 'attendance' not in db['id_profiles'][str(author.id)].keys():
        db['id_profiles'][str(author.id)]['attendance'] = {
            'last_checked_in': '',
            'last_checked_out': '',
        }
    if 'activated' not in db['id_profiles'][str(author.id)]:
        db['id_profiles'][str(author.id)]['activated'] = 1


async def set_profile_if_missing(author):
    if 'id_profiles' not in db.keys():
        db['id_profiles'] = {}
    if str(author.id) not in db['id_profiles'].keys():
        db['id_profiles'][str(author.id)] = {}
    set_attendance_format_if_missing(author)
