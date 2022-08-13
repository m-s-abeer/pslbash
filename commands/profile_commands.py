from utils import encrypt_string


async def set_profile_key_value(message, user_data, key, value):
    if key == "email":
        user_data.email = value
        await message.channel.send(f"{user_data.mention} Your {key} is set")
        await message.delete()
    elif key == "pass":
        user_data.password = encrypt_string(value.strip())
        await message.channel.send(f"{user_data.mention} Your {key} is set")
        await message.delete()
    elif key == "activate":
        user_data.disabled = False
        await message.channel.send(f"{user_data.mention} Your account activated. Try checking in now.")
        await show_personal_data(message, user_data)
    elif key == "vacation":
        value = bool(int(value))
        user_data.vacation = value
        await message.channel.send(f"{user_data.mention} Your vacation mode is set to {value}. Check your profile.")
        await show_personal_data(message, user_data)
    elif key == "cin_from":
        try:
            values = value.split(" ")
            hour = int(values[0])
            minute = int(values[1])

            user_data.checkin_after = (hour, minute)
            await message.channel.send(f"{user_data.mention} Your {key} is set")
        except:
            await message.channel.send("Invalid command!")
    elif key == "cout_from":
        try:
            values = value.split(" ")
            hour = int(values[0])
            minute = int(values[1])

            user_data.checkout_after = (hour, minute)
            await message.channel.send(f"{user_data.mention} Your {key} is set")
        except:
            await message.channel.send("Invalid command!")
    else:
        await message.channel.send("Invalid command!")


async def show_personal_data(message, user_data):
    msg = f">>>>>>>>>>{user_data.mention}<<<<<<<<<<\n"
    msg += f"Showing your profile info\n"
    msg += f"** ID:** {user_data.uuid}\n"
    msg += f"** Email:** {user_data.email}\n"
    msg += f"** Disabled:** {user_data.disabled}\n"
    msg += "=========================\n"

    try:
        checkin_start_hh = user_data.checkin_after["hh"]
        checkin_start_mm = user_data.checkin_after["mm"]
        checkout_start_hh = user_data.checkout_after["hh"]
        checkout_start_mm = user_data.checkout_after["mm"]
        msg += f"** Schedule type:** Personal\n"
        msg += f"** Checkin start:** {checkin_start_hh:02d}:{checkin_start_mm:02d}\n"
        msg += f"** Checkout start:** {checkout_start_hh:02d}:{checkout_start_mm:02d}\n"
    except:
        msg += f"** Schedule type:** Global\n"

    try:
        last_cin_date = user_data.last_checkin["date"]
        last_cin_hh, last_cin_mm = [int(x) for x in user_data.last_checkin["time"].split(":")[:2]]
        last_cout_date = user_data.last_checkout["date"]
        last_cout_hh, last_cout_mm = [int(x) for x in user_data.last_checkout["time"].split(":")[:2]]
        msg += "=========================\n"
        msg += f"** Vacation Mode:** {bool(user_data.vacation)}\n"
        msg += f"** Last Checkin:** {last_cin_date} {last_cin_hh:02d}:{last_cin_mm:02d}\n"
        msg += f"** Last Checkout:** {last_cout_date} {last_cout_hh:02d}:{last_cout_mm:02d}\n"
    except:
        pass
    msg += f"<<<<<<<<<<{user_data.mention}>>>>>>>>>>\n\n"

    await message.channel.send(msg)
