from commands.config_commands import set_config_key_value
from commands.mylist_commands import process_mylist_commands
from commands.profile_commands import set_profile_key_value, show_personal_data
from commands.random_replies import send_random_reply
from db_app.utils import get_all_user_data
from utils import get_command_and_text_pair
from scheduler.checkin_checkout_services import checkin, checkout, checkin_all, checkout_all


async def process_command(message, user_data, text):
    command, text = get_command_and_text_pair(text)

    if command == "set":
        key, value = get_command_and_text_pair(text)
        await set_profile_key_value(message, user_data, key, value)
    elif command == "mylist":
        await process_mylist_commands(message, user_data, text)
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
        if key == "profile":
            if value and "all" in value:
                all_users = await get_all_user_data()
                for user in all_users:
                    await show_personal_data(message, user)
            else:
                await show_personal_data(message, user_data)
    elif command == "test":
        print(command)
    else:
        await send_random_reply(user_data, message)
