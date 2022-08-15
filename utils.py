import requests
import os
from Crypto.Cipher import AES
import base64
from datetime import datetime, timezone, timedelta
from bot_obj import bot


def get_bangladeshi_datetime():
    bangladeshi_datetime = datetime.now(timezone(timedelta(hours=6)))
    return bangladeshi_datetime


def get_3_char_weekday_today():
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    return days[get_bangladeshi_datetime().weekday()]


def get_cur_bangladeshi_date():
    return get_bangladeshi_datetime().date()


def get_cur_bangladeshi_time():
    return get_bangladeshi_datetime().time()


def time_in_range(start_time, end_time, cur_time):
    return start_time <= cur_time and cur_time <= end_time


def get_command_and_text_pair(message):
    res = message.split(" ", 1)
    com, text = res[0], None
    if len(res) == 2:
        text = res[1]
    return com, text


async def ping_heroku():
    # requests.get('https://pslhobasher.herokuapp.com')
    requests.post("https://pslhobasher.herokuapp.com/pslbasher/checkin/")
    requests.post("https://pslhobasher.herokuapp.com/pslbasher/checkout/")


def stringToBase64(s):
    return base64.b64encode(s.encode("ISO-8859-1"))


def base64ToString(b):
    return base64.b64decode(b).decode("ISO-8859-1")


def time_difference_in_mins(start_time, end_time):
    st_time_in_mins = start_time.hour * 60 + start_time.minute
    en_time_in_mins = end_time.hour * 60 + end_time.minute

    return int(en_time_in_mins - st_time_in_mins)


def encrypt_string(text):
    obj = AES.new(os.getenv("EN_KEY"), AES.MODE_CBC, "This is an IV456")
    enc_bytes = obj.encrypt(text * 16)
    enc_string = base64ToString(base64.b64encode(enc_bytes))
    return str(enc_string)


def decrypt_string(text):
    dec_bytes = base64.b64decode(stringToBase64(text))
    obj = AES.new(os.getenv("EN_KEY"), AES.MODE_CBC, "This is an IV456")
    data = obj.decrypt(dec_bytes).decode("ISO-8859-1")
    return str(data[: len(data) // 16])


def post_data(endpoint, data):
    response = requests.post(endpoint, data=data)
    print(f"Response status: {response.status_code}")

    if response.status_code >= 400:
        print(f"Post request failed!")
    return response


async def get_user_obj_with_id(user_id):
    user_id = int(user_id)
    client = bot.get_bot()
    try:
        user_obj = await client.fetch_user(user_id)
    except:
        print(f"user {user_id} not found!")
        # from db_app import remove_profile_with_id
        # await remove_profile_with_id(user_id)
        return None
    return user_obj


async def get_user_mention_string(user_id):
    user_obj = await get_user_obj_with_id(user_id)
    if user_obj:
        return user_obj.mention
