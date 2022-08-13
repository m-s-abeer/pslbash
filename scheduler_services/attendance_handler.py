from db_handler import set_last_checked_in, set_last_checked_out, get_all_user_data
from utils import (
    post_data,
    decrypt_string,
    get_cur_bangladeshi_date,
    get_cur_bangladeshi_time,
    time_in_range,
    time_difference_in_mins,
    ping_heroku,
)
from datetime import time
import asyncio


async def deactivate_till_updated(channel, user_data):
    await channel.send(
        f"{user_data.mention} Your email/pass is not set properly. Deactivating your automated attendance till you update email/pass and activate again."
    )
    user_data.disabled = True


async def checkin(channel, user_data):
    try:
        email = user_data.email
        password = user_data.password
        if not email or not password:
            raise
    except:
        await deactivate_till_updated(channel, user_data)
        return
    await channel.send(f"{user_data.mention} Checking in " + user_data.email)

    response = post_data(
        "https://pslhobasher.herokuapp.com/pslbasher/checkin/",
        {"username": email, "password": decrypt_string(password)},
    )

    if response.status_code == 200:
        await set_last_checked_in(user_data)
        await channel.send(f"{user_data.mention} Checked in successfully! Have a nice day!")
    else:
        await channel.send(f"{user_data.mention} Check in failed with errors " + str(response.status_code))


async def checkout(channel, user_data):
    try:
        email = user_data.email
        password = user_data.password
        if not email or not password:
            raise
    except:
        await deactivate_till_updated(channel, user_data)
        return

    await channel.send(f"{user_data.mention} Checking out " + user_data.email)

    response = post_data(
        "https://pslhobasher.herokuapp.com/pslbasher/checkout/",
        {"username": email, "password": decrypt_string(password)},
    )

    if response.status_code == 200:
        await set_last_checked_out(user_data)
        await channel.send(f"{user_data.mention} Checked out successfully! Seeya!")
    else:
        await channel.send(f"{user_data.mention} Check out failed with errors " + str(response.status_code))


async def checkin_all(channel):
    cur_date = get_cur_bangladeshi_date()
    users_list = await get_all_user_data()
    for user_data in users_list:
        try:
            if (
                user_data.disabled is False
                and user_data.vacation is False
                and user_data.last_checkin["date"] != str(cur_date)
            ):
                await checkin(channel, user_data)
        except:
            pass


async def checkout_all(channel):
    cur_date = get_cur_bangladeshi_date()
    users_list = await get_all_user_data()
    for user_data in users_list:
        try:
            if (
                user_data.disabled is False
                and user_data.vacation is False
                and user_data.last_checkout["date"] != str(cur_date)
            ):
                await checkout(channel, user_data)
        except:
            pass


async def clear_checkin_all(channel):
    users_list = await get_all_user_data()
    for user in users_list:
        user.last_checkin = ("0000-00-00", "00:00:00")
    await channel.send("Cleared all last checkin history")


async def clear_checkout_all(channel):
    users_list = await get_all_user_data()
    for user in users_list:
        user.last_checkout = ("0000-00-00", "00:00:00")
    await channel.send("Cleared all last checkout history")


async def scheduled_checkin_checkout(channel):
    g_checkin_start_time = time(hour=8, minute=45)
    g_checkin_end_time = time(hour=9, minute=30)

    g_checkout_start_time = time(hour=18, minute=5)
    g_checkout_end_time = time(hour=19, minute=5)

    cur_date = get_cur_bangladeshi_date()
    cur_time = get_cur_bangladeshi_time()
    users_list = await get_all_user_data()

    for user in users_list:
        if user.disabled is False and user.vacation is False:
            try:
                if user.last_checkin and user.last_checkin["date"] != str(cur_date):
                    checkin_start_hh = user.checkin_after["hh"]
                    checkin_start_mm = user.checkin_after["mm"]
                    checkin_start_time = time(hour=checkin_start_hh, minute=checkin_start_mm)
                    checkin_end_time = time(hour=checkin_start_hh + 1, minute=checkin_start_mm)

                    before_checkin_mins = time_difference_in_mins(cur_time, checkin_start_time)

                    if 0 <= before_checkin_mins <= 15:
                        await ping_heroku()

                    if time_in_range(checkin_start_time, checkin_end_time, cur_time):
                        asyncio.create_task(checkin(channel, user))

            except:
                before_checkin_mins = time_difference_in_mins(cur_time, g_checkin_start_time)

                if 0 <= before_checkin_mins <= 15:
                    await ping_heroku()

                if time_in_range(g_checkin_start_time, g_checkin_end_time, cur_time):
                    asyncio.create_task(checkin(channel, user))

            try:
                if user.last_checkout and user.last_checkout["date"] != str(cur_date):
                    checkout_start_hh = user.checkout_after["hh"]
                    checkout_start_mm = user.checkout_after["mm"]
                    checkout_start_time = time(hour=checkout_start_hh, minute=checkout_start_mm)
                    checkout_end_time = time(hour=checkout_start_hh + 1, minute=checkout_start_mm)

                    before_checkout_mins = time_difference_in_mins(cur_time, checkout_start_time)

                    if 0 <= before_checkout_mins <= 15:
                        await ping_heroku()

                    if time_in_range(checkout_start_time, checkout_end_time, cur_time):
                        asyncio.create_task(checkout(channel, user))

            except:
                before_checkout_mins = time_difference_in_mins(cur_time, g_checkout_start_time)

                if 0 <= before_checkout_mins <= 15:
                    await ping_heroku()

                if time_in_range(g_checkout_start_time, g_checkout_end_time, cur_time):
                    asyncio.create_task(checkout(channel, user))
