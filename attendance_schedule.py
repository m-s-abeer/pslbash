from discord.ext import tasks, commands
from utils import get_3_char_weekday_today, get_cur_bangladeshi_time, time_in_range
from db_handler import get_keys, get_broadcast_channel, get_is_schedule_active, get_cur_bangladeshi_date, get_last_holiday_message_sent, set_last_holiday_message_sent
from replit import db
from datetime import time
from attendance_handler import checkin_all, checkout_all, scheduled_checkin_checkout


class AttendanceSchedule(commands.Cog):
    def get_channel(self):
        channel = self.bot.get_channel(int(get_broadcast_channel()))
        return channel

    def __init__(self, bot):
        self.bot = bot
        self.attendance_auto.start()

    def cog_unload(self):
        self.attendance_auto.cancel()

    @tasks.loop(minutes=5)
    async def attendance_auto(self):
        if db['config']['auto_schedule'] == 1:
            weekday = get_3_char_weekday_today()
            cur_time = get_cur_bangladeshi_time()
            cur_date = str(get_cur_bangladeshi_date())

            print(f"Last checked at: {str(cur_date)} {cur_time}")

            if weekday not in ['FRI', 'SAT']:
                await scheduled_checkin_checkout(self.get_channel())

            if get_is_schedule_active(
            ) and not cur_date == get_last_holiday_message_sent(
            ) and time_in_range(time(hour=20, minute=30),
                                time(hour=21, minute=00),
                                cur_time) and weekday == 'THU':
                await self.get_channel().send(db['config']['weekend_message'])
                set_last_holiday_message_sent(cur_date)

    @attendance_auto.before_loop
    async def before_start(self):
        print('waiting...')
        await self.bot.wait_until_ready()
