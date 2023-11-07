from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return [
        f"Мяу!",
        Image('cat.png'),
    ]


run_bot()
