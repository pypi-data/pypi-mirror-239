from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return f"Мяу!"
    # return f"Все говорят «{msg}», а ты купи слона!"


run_bot()
