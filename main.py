import os
from keep_alive import keep_alive
from utils import get_command_and_text_pair
from command_processor import process_command
from attendance_schedule import AttendanceSchedule
from replit import db
from db_handler import set_profile_if_missing, get_broadcast_channel
import asyncio
from bot_obj import bot

keep_alive()

client = bot.get_bot()


def help_info():
    return '''
  PSL HO Basher bot commands:
  ==================================
  -> pslbash show profile - To view your profile info
  -> pslbash set email <your_psl_ho_email> - To set your email
  -> pslbash set pass <your_psl_ho_password> - To set your password(saved encrypted)
  -> pslbash set activated <0_or_1> - To activate auto_schedule, set 1 and 0 otherwise
  -> pslbash set checkin_start <HH> <MM> - To set personal start time of checkin, the time is in UTC+0600 and 24hours format. Avoid using times close to midnight.
  -> pslbash set checkout_start <HH> <MM> - To set personal start time of checkout, the time is in UTC+0600 and 24hours format. Avoid using times close to midnight.
  -> pslbash set profile - To copy your profile from old username based profile
  -> pslbash checkin - To checkin using your provided email and pass
  -> pslbash checkout - To checkout using your provided email and pass

  PSL HO Basher config commands:
  ==================================
  -> pslbash config channel_id <channel_id_for_scheduled_report> - To set global report channel
  -> pslbash config auto_schedule <0_or_1> - To start auto checkin checkout for everyone set 1 and 0 otherwise
  -> pslbash config clr_all_cin_history - To clear each user's checkin history
  -> pslbash config clr_all_cout_history - To clear each user's checkout history

  * Global checkin starts and ends between 08:45 - 09:30
  * Global checkout starts and ends between 18:05 - 17:05
  * Attendance scheduler will run every 5 minutes
  '''


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    if 'config' not in db.keys():
        db['config'] = {}
    if 'channel_id' not in db['config'].keys():
        db['config']['channel_id'] = 856779503916154888
    if 'auto_schedule' not in db['config'].keys():
        db['config']['auto_schedule'] = 1

    AttendanceSchedule(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    author = message.author
    
    if message.content.startswith('pslbash'):
        await set_profile_if_missing(author)
        command, text = get_command_and_text_pair(message.content)
        if 'pass' not in message.content:
          print(message.author, message.content)
        if text == None:
            await message.channel.send(help_info())
        else:
            await process_command(message, author, text)


asyncio.run(client.run(os.getenv('TOKEN')))
