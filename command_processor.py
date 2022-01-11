import random
from replit import db
from utils import encrypt_string, get_command_and_text_pair
from attendance_handler import checkin, checkin_all, checkout_all, checkout, clear_checkin_all, clear_checkout_all
from db_handler import get_last_checked_in, get_last_checked_out, get_is_active, get_email


async def set_profile_key_value(message, author, key, value):

    if key in ["email", "pass", "activated"]:
        if key not in db["id_profiles"][str(author.id)].keys():
            db["id_profiles"][str(author.id)][key] = ""

        if key.startswith("pass"):
            pw = encrypt_string(value)
            db["id_profiles"][str(author.id)][key] = pw
        else:
            db["id_profiles"][str(author.id)][key] = value
        await message.channel.send(f"{author.mention} Your {key} is set")
        await message.delete()
    elif key in ["checkin_start", "checkout_start"]:
        try:
            values = value.split(" ")
            hour = int(values[0])
            minute = int(values[1])

            db["id_profiles"][str(author.id)][key + "_hh"] = hour
            db["id_profiles"][str(author.id)][key + "_mm"] = minute
            await message.channel.send(f"{author.mention} Your {key} is set")
        except:
            await message.channel.send("Invalid command 2!")
    elif key == "profile":
        db["id_profiles"][str(author.id)] = db["profiles"][str(author)]
        await message.channel.send(f"{author.mention} successful!")
    else:
        await message.channel.send("Invalid command!")


async def set_config_key_value(message, author, key, value):

    if key in ["channel_id", "auto_schedule", "weekend_message"]:
        if key not in db["config"].keys():
            db["config"][key] = ""

        if key == "weekend_message":
            db["config"][key] = value
        else:
            db["config"][key] = int(value)

        await message.channel.send(f"{author.mention} Global {key} is set to " + f'"{value}"')
    elif key in "clr_all_cin_history":
        await clear_checkin_all(message.channel)
    elif key in "clr_all_cout_history":
        await clear_checkout_all(message.channel)
    else:
        await message.channel.send("Invalid command!")


async def show_personal_data(message, author, key, value):
    if key == "profile":
        msg = f"{author.mention}\n\n"
        msg += f"**ID:** {author.id}\n"
        msg += f"**Tag:** {str(author)}\n"
        msg += f"**Email:** {get_email(author)}\n"
        msg += "==============================\n"

        try:
            checkin_start_hh = db["id_profiles"][str(author.id)]["checkin_start_hh"]
            checkin_start_mm = db["id_profiles"][str(author.id)]["checkin_start_mm"]
            checkout_start_hh = db["id_profiles"][str(author.id)]["checkout_start_hh"]
            checkout_start_mm = db["id_profiles"][str(author.id)]["checkout_start_mm"]
            msg += f"**Schedule type:** Personal\n"
            msg += f"**Checkin start:** {checkin_start_hh}:{checkin_start_mm}\n"
            msg += f"**Checkout start:** {checkout_start_hh}:{checkout_start_mm}\n"
        except:
            msg += f"**Schedule type:** Global\n"

        msg += "==============================\n"
        msg += f"**Auto Schedule:** {get_is_active(author)}\n"
        msg += f"**Last Checkin:** {get_last_checked_in(author)}\n"
        msg += f"**Last Checkout:** {get_last_checked_out(author)}\n"

        await message.channel.send(msg)


async def process_command(message, author, text):

    command, text = get_command_and_text_pair(text)

    if command == "set":
        key, value = get_command_and_text_pair(text)
        await set_profile_key_value(message, author, key, value)
    elif command == "checkin":
        if text and "all" in text:
            await checkin_all(message.channel)
        else:
            await checkin(message.channel, author)
    elif command == "checkout":
        if text and "all" in text:
            await checkout_all(message.channel)
        else:
            await checkout(message.channel, author)
    elif command == "config":
        key, value = get_command_and_text_pair(text)
        await set_config_key_value(message, author, key, value)
    elif command == "show":
        key, value = get_command_and_text_pair(text)
        await show_personal_data(message, author, key, value)
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
        await message.channel.send(f"{author.mention} {random_reply}")
