import os

from data_classes.default_config_handler import DefaultConfigHandler
from keep_alive import keep_alive
from data_classes.user_data_repo import UserData
from utils import get_command_and_text_pair
from command_processor import process_command
from attendance_schedule import AttendanceSchedule
import asyncio
from bot_obj import bot

keep_alive()

client = bot.get_bot()


def help_info():
    return """
**PSL Bash bot commands:**
**==================================**
**pslbash show profile**: To view your profile info
**pslbash set email <your_psl_ho_email>**: To set your email
**pslbash set pass <your_psl_ho_password>**: To set your password(saved encrypted)
**pslbash set activate**: To activate your scheduling account if disabled automatically
**pslbash set vacation B**: To activate vacation mode, set B as 1 or 0 otherwise
**pslbash set cin_from HH MM**: To set personal start time of checkin, the time is in UTC+0600 and 24hours format.
**pslbash set cout_from HH MM**: To set personal start time of checkout, the time is in UTC+0600 and 24hours format.
**pslbash set profile**: To copy your profile from old username based profile
**pslbash cin**: To checkin using your provided email and pass
**pslbash cout**: To checkout using your provided email and pass

PSL HO Basher config commands:
==================================
**pslbash config auto_schedule B**: To start auto checkin checkout for everyone set B as 1 or 0 otherwise
**pslbash config clr_all_cin_history**: To clear each user's checkin history
**pslbash config clr_all_cout_history**: To clear each user's checkout history

* Global checkin starts and ends between 08:45 - 09:30
* Global checkout starts and ends between 18:05 - 17:05
* Attendance scheduler will run every 5 minutes
  """


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    DefaultConfigHandler().set_init_config()
    AttendanceSchedule(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    author = message.author

    if message.content.startswith("pslbash"):
        user_data = UserData(author.id)
        command, text = get_command_and_text_pair(message.content)
        if "pass" not in message.content:
            print(message.author, message.content)
        if text is None:
            await message.channel.send(help_info())
        else:
            await process_command(message, user_data, text)


asyncio.run(client.run(os.getenv("DISCORD_TOKEN")))
