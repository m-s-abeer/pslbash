from commands.random_replies import send_random_reply
from utils import get_command_and_text_pair


async def process_mylist_commands(message, user_data, value):
    if value.strip() == "":
        # TODO: show mylist command details
        pass
    else:
        cmd, msg = get_command_and_text_pair(value)
        if cmd == "list":
            # TODO: show the whole list under current profile
            pass
        elif cmd == "add":
            # TODO: add email and password to mylist
            pass
        elif cmd == "del":
            # TODO: delete an item by it's _id
            pass
        elif cmd == "disable":
            # TODO: disable an item by it's _id
            pass
        else:
            await send_random_reply(user_data, message)
