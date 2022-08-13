from scheduler_services.attendance_handler import clear_checkin_all, clear_checkout_all
from data_classes.default_config_handler import DefaultConfigHandler


async def set_config_key_value(message, user_data, key, value):
    if key == "channel_id":
        DefaultConfigHandler().channel_id = int(value)
        await message.channel.send(f"{user_data.mention} Global {key} is set to {int(value)}")
    elif key == "auto_schedule":
        value = bool(int(value))
        DefaultConfigHandler().auto_schedule = value
        await message.channel.send(f"{user_data.mention} Global {key} is set to {value}")
    elif key == "clr_all_cin_history":
        await clear_checkin_all(message.channel)
    elif key == "clr_all_cout_history":
        await clear_checkout_all(message.channel)
    else:
        await message.channel.send("Invalid command!")
