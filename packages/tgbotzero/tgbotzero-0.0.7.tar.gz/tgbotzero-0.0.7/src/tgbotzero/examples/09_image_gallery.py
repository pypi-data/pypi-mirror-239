from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return [
        f"Мяу-гав!",
        Image('cat.png'),
        Image('dog.png'),
        Button('Класс!', 'btn')
    ]

def on_button_btn(data):
    return 'Ага!'

run_bot()
