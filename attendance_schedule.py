from discord.ext import tasks, commands
from db_ops.default_config_handler import DefaultConfigHandler
from utils import get_3_char_weekday_today, get_cur_bangladeshi_time
from db_handler import (
    get_broadcast_channel,
    get_cur_bangladeshi_date,
)
from attendance_handler import scheduled_checkin_checkout


class AttendanceSchedule(commands.Cog):
    def get_channel(self):
        channel = self.bot.get_channel(int(get_broadcast_channel()))
        return channel

    def __init__(self, bot):
        self.bot = bot
        self.attendance_auto.start()

    def cog_unload(self):
        self.attendance_auto.cancel()

    # TODO: take loop cycle from default_config
    @tasks.loop(minutes=5)
    async def attendance_auto(self):
        def_conf = DefaultConfigHandler()

        if def_conf.auto_schedule is True:
            weekday = get_3_char_weekday_today()
            cur_time = get_cur_bangladeshi_time()
            cur_date = str(get_cur_bangladeshi_date())

            print(f"Last checked at: {str(cur_date)} {cur_time}")

            if weekday not in ["FRI", "SAT"]:
                await scheduled_checkin_checkout(self.get_channel())

            # TODO: Re-implement holiday wish
            # if (
            #         not cur_date == get_last_holiday_message_sent()
            #         and time_in_range(time(hour=20, minute=30), time(hour=21, minute=00), cur_time)
            #         and weekday == "THU"
            # ):
            #     await self.get_channel().send("Have a nice weekend everyone!")
            #     set_last_holiday_message_sent(cur_date)

    @attendance_auto.before_loop
    async def before_start(self):
        print("waiting...")
        await self.bot.wait_until_ready()
