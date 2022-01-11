from replit import db
from db_handler import get_all_users, get_last_checked_in, get_last_checked_out, set_last_checked_in, set_last_checked_out, set_attendance_format_if_missing, get_is_active, clear_last_checked_in, clear_last_checked_out
from utils import post_data, decrypt_string, get_cur_bangladeshi_date, get_cur_bangladeshi_time, time_in_range, time_difference_in_mins, ping_heroku
import random
from datetime import time
import asyncio


async def deactivate_till_updated(channel, author):
    await channel.send(
        f'{author.mention} Your email/pass is not set properly. Deactivating your automated attendance till you update email/pass and activate again.'
    )
    db['id_profiles'][str(author.id)]['activated'] = 0


async def checkin(channel, author):
    try:
        email = db['id_profiles'][str(author.id)]['email']
        password = db['id_profiles'][str(author.id)]['pass']
    except:
        await deactivate_till_updated(channel, author)
        return

    if not email or not password:
        await deactivate_till_updated(channel, author)
    else:
        await channel.send(f'{author.mention} Checking in ' +
                           db['id_profiles'][str(author.id)]['email'])

        response = post_data(
            'https://pslhobasher.herokuapp.com/pslbasher/checkin/', {
                'username': email,
                'password': decrypt_string(password)
            })

        if (response.status_code == 200):
            await set_last_checked_in(author)
            await channel.send(
                f'{author.mention} Checked in successfully! Have a nice day!')
        else:
            await channel.send(
                f'{author.mention} Check in failed with errors ' +
                str(response.status_code))


async def checkout(channel, author):
    try:
        email = db['id_profiles'][str(author.id)]['email']
        password = db['id_profiles'][str(author.id)]['pass']
    except:
        await deactivate_till_updated(channel, author)
        return

    if not email or not password:
        await deactivate_till_updated(channel, author)
    else:
        await channel.send(f'{author.mention} Checking out ' +
                           db['id_profiles'][str(author.id)]['email'])

        response = post_data(
            'https://pslhobasher.herokuapp.com/pslbasher/checkout/', {
                'username': email,
                'password': decrypt_string(password)
            })

        if (response.status_code == 200):
            await set_last_checked_out(author)
            await channel.send(
                f'{author.mention} Checked out successfully! Seeya!')
        else:
            await channel.send(
                f'{author.mention} Check out failed with errors ' +
                str(response.status_code))


async def checkin_all(channel):
    cur_date = get_cur_bangladeshi_date()
    users_list = await get_all_users()
    for user in users_list:
        set_attendance_format_if_missing(user)
        if get_is_active(user) and get_last_checked_in(user) != str(cur_date):
            await checkin(channel, user)


async def checkout_all(channel):
    cur_date = get_cur_bangladeshi_date()
    users_list = await get_all_users()
    for user in users_list:
        set_attendance_format_if_missing(user)
        if get_is_active(user) and get_last_checked_out(user) != str(cur_date):
            await checkout(channel, user)


async def clear_checkin_all(channel):
    users_list = await get_all_users()
    for user in users_list:
        set_attendance_format_if_missing(user)
        await clear_last_checked_in(user)
    await channel.send('Cleared all last checkin history')


async def clear_checkout_all(channel):
    users_list = await get_all_users()
    for user in users_list:
        set_attendance_format_if_missing(user)
        await clear_last_checked_out(user)
    await channel.send('Cleared all last checkout history')


async def scheduled_checkin(channel, user, type_of_sc='globally'):

    # await channel.send(
    #     f'Trying {type_of_sc} scheduled checkin for {user.mention}'
    # )
    await checkin(channel, user)


async def scheduled_checkout(channel, user, type_of_sc='globallly'):

    # await channel.send(
    #     f'Trying {type_of_sc} scheduled checkout for {user.mention}'
    # )
    await checkout(channel, user)


async def scheduled_checkin_checkout(channel):

    g_checkin_start_time = time(hour=8, minute=45)
    g_checkin_end_time = time(hour=9, minute=30)

    g_checkout_start_time = time(hour=18, minute=5)
    g_checkout_end_time = time(hour=19, minute=5)

    cur_date = get_cur_bangladeshi_date()
    cur_time = get_cur_bangladeshi_time()
    users_list = await get_all_users()
    for user in users_list:
        set_attendance_format_if_missing(user)
        if get_is_active(user):
            if get_last_checked_in(user) != str(cur_date):
                try:
                    checkin_start_hh = db['id_profiles'][str(
                        user.id)]['checkin_start_hh']
                    checkin_start_mm = db['id_profiles'][str(
                        user.id)]['checkin_start_mm']
                    checkin_start_time = time(hour=checkin_start_hh,
                                              minute=checkin_start_mm)
                    checkin_end_time = time(hour=checkin_start_hh + 1,
                                            minute=checkin_start_mm)

                    before_checkin_mins = time_difference_in_mins(
                        cur_time, checkin_start_time)

                    if (before_checkin_mins >= 0
                            and before_checkin_mins <= 15):
                        await ping_heroku()

                    if time_in_range(checkin_start_time, checkin_end_time,
                                     cur_time):
                        asyncio.create_task(
                            scheduled_checkin(channel, user, 'personally'))

                except:

                    before_checkin_mins = time_difference_in_mins(
                        cur_time, g_checkin_start_time)

                    if (before_checkin_mins >= 0
                            and before_checkin_mins <= 15):
                        await ping_heroku()

                    if time_in_range(g_checkin_start_time, g_checkin_end_time,
                                     cur_time):
                        asyncio.create_task(scheduled_checkin(channel, user))
            if get_last_checked_out(user) != str(cur_date):
                try:
                    checkout_start_hh = db['id_profiles'][str(
                        user.id)]['checkout_start_hh']
                    checkout_start_mm = db['id_profiles'][str(
                        user.id)]['checkout_start_mm']
                    checkout_start_time = time(hour=checkout_start_hh,
                                               minute=checkout_start_mm)
                    checkout_end_time = time(hour=checkout_start_hh + 1,
                                             minute=checkout_start_mm)

                    before_checkout_mins = time_difference_in_mins(
                        cur_time, checkout_start_time)

                    if (before_checkout_mins >= 0
                            and before_checkout_mins <= 15):
                        await ping_heroku()

                    if time_in_range(checkout_start_time, checkout_end_time,
                                     cur_time):
                        asyncio.create_task(
                            scheduled_checkout(channel, user, 'personally'))

                except:

                    before_checkout_mins = time_difference_in_mins(
                        cur_time, g_checkout_start_time)

                    if (before_checkout_mins >= 0
                            and before_checkout_mins <= 15):
                        await ping_heroku()

                    if time_in_range(g_checkout_start_time,
                                     g_checkout_end_time, cur_time):
                        asyncio.create_task(scheduled_checkout(channel, user))
