from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return 'Жду картинку с подписью!'


def on_image(msg: str, img: Image):
    return [
        'Вот твоё фото',
        img,
    ]

run_bot()
