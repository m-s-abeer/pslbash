from db_app.utils import set_last_checked_in, set_last_checked_out, get_all_user_data
from utils import post_data, decrypt_string, get_cur_bangladeshi_date


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
