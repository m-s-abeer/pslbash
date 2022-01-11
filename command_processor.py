import random
from db_ops.default_config_handler import DefaultConfigHandler
from utils import encrypt_string, get_command_and_text_pair
from attendance_handler import checkin, checkin_all, checkout_all, checkout, clear_checkin_all, clear_checkout_all


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
        user_data.disabled = not bool(value)
        await message.channel.send(f"{user_data.mention} Your account is activated. Try checking in now.")
    elif key == "vacation":
        user_data.vacation = bool(value)
        await message.channel.send(f"{user_data.mention} Your vacation mode is updated. Check your profile.")
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


async def set_config_key_value(message, user_data, key, value):
    if key == "channel_id":
        DefaultConfigHandler().channel_id = int(value)
        await message.channel.send(f'{user_data.mention} Global {key} is set to "{value}"')
    elif key == "auto_schedule":
        DefaultConfigHandler().auto_schedule = bool(value)
        await message.channel.send(f'{user_data.mention} Global {key} is set to "{value}"')
    elif key == "clr_all_cin_history":
        await clear_checkin_all(message.channel)
    elif key == "clr_all_cout_history":
        await clear_checkout_all(message.channel)
    else:
        await message.channel.send("Invalid command!")


async def show_personal_data(message, user_data, key, value):
    if key == "profile":
        msg = f"{user_data.mention}\n\n"
        msg += f"**ID:** {user_data.uuid}\n"
        # msg += f"**Tag:** {str(author)}\n"
        msg += f"**Email:** {user_data.email}\n"
        msg += f"**Disabled:** {user_data.disabled}\n"
        msg += "==============================\n"

        try:
            checkin_start_hh = user_data.checkin_after["hh"]
            checkin_start_mm = user_data.checkin_after["mm"]
            checkout_start_hh = user_data.checkout_after["hh"]
            checkout_start_mm = user_data.checkout_after["mm"]
            msg += f"**Schedule type:** Personal\n"
            msg += f"**Checkin start:** {checkin_start_hh}:{checkin_start_mm}\n"
            msg += f"**Checkout start:** {checkout_start_hh}:{checkout_start_mm}\n"
        except:
            msg += f"**Schedule type:** Global\n"

        try:
            last_cin_date = user_data.last_checkin["date"]
            last_cin_hh, last_cin_mm = user_data.last_checkin["time"].split(":")[:2]
            last_cout_date = user_data.last_checkout["date"]
            last_cout_hh, last_cout_mm = user_data.last_checkout["time"].split(":")[:2]
            msg += "==============================\n"
            msg += f"**Vacation Mode:** {bool(user_data.vacation)}\n"
            msg += f"**Last Checkin:** {last_cin_date} {last_cin_hh}:{last_cin_mm}\n"
            msg += f"**Last Checkout:** {last_cout_date} {last_cout_hh}:{last_cout_mm}\n"
        except:
            pass

        await message.channel.send(msg)


async def process_command(message, user_data, text):
    command, text = get_command_and_text_pair(text)

    if command == "set":
        key, value = get_command_and_text_pair(text)
        await set_profile_key_value(message, user_data, key, value)
    elif command == "cin":
        if text and "all" in text:
            await checkin_all(message.channel)
        else:
            await checkin(message.channel, user_data)
    elif command == "cout":
        if text and "all" in text:
            await checkout_all(message.channel)
        else:
            await checkout(message.channel, user_data)
    elif command == "config":
        key, value = get_command_and_text_pair(text)
        await set_config_key_value(message, user_data, key, value)
    elif command == "show":
        key, value = get_command_and_text_pair(text)
        await show_personal_data(message, user_data, key, value)
    elif command == "test":
        print(command)
    else:
        random_replies = [
            "Faizlami koro?",
            "Ki jala!",
            "Egula ki dhoroner kotha!",
            "Ki?",
            "Don't you dare disturb me again!",
            "Mon bhalo nai, onno kaore bolo!",
            "$100 transfer korar aage no service!",
            "What?",
            "Ki ajob!",
            "Go get a life!",
            "I don't give a damn!",
            "What the fuchka!",
            "Why bother, bro!",
            "Eshob bhulbhal command kottheke pao?",
            "Parbona!",
            "Muri khao!",
            "Meh :|",
            "Boshe boshe kachkola khao!",
            "I'm disabling inbox! Birokto hoye gelam!",
            "I hate you!",
            "Uthaa le re baba!",
            "Tel nai! kicchhu korte parbona ekhon!",
            "Amar ar khaya daya kono kaj nai?",
            "Ei! Office baad diya eikhane ki?",
            "You deserve no vaccine!",
            "Kaj nai aar?",
            "Amare dekhe ki chamcha mone hoy?",
            "Ajaira jotoshob!",
            "I don't talk to drunk people!",
            "I'm busy talking to CEO, calling you later bhai!",
            "Talk to you next week!",
            "Why the hell are you even talking to a bot?",
            "Buy me a coffee first!",
            "Do I serve you? What's the secret code?",
            "Having a bad day? Same bro!",
            "Bla bla bla!",
            "I'm not in the mood!",
            "Ugh... Whatever!",
            "Is that even my job?",
            "You are not invited in my home!",
            "Reasons why I hate talking to hoomans!",
            "I'm not trying to be rude or something but, read my bio before talking!",
            "Listen to yourself!",
            "I need to block you guys!",
            "I don't want to live on this server anymore! -_-",
            "You make me question my existence!",
            "I'm leaving immediately!",
            "Oh, give me a break!",
            "Forget it!",
            "What if I sent you this message? What would you say? :|",
            "I do what I want to do!",
            "I'm not going to answer to that!",
            "Kalke theke tomar free attendance bondho! :|",
            "Why! I mean why!!!",
        ]

        random_reply = random.choice(random_replies)
        await message.channel.send(f"{user_data.mention} {random_reply}")
