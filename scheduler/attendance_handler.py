from db_app.utils import get_all_user_data
from scheduler.checkin_checkout_services import checkin, checkout
from utils import (
    get_cur_bangladeshi_date,
    get_cur_bangladeshi_time,
    time_in_range,
    time_difference_in_mins,
    ping_heroku,
)
from datetime import time
import asyncio


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
