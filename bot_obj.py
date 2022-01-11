import discord


class SingletonBot:
    _bot = None

    def __init__(self, *args, **kwargs):
        if not self._bot:
            self._bot = discord.Client()

    def get_bot(self):
        return self._bot


bot = SingletonBot()
