import random


async def send_random_reply(user_data, message):
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
