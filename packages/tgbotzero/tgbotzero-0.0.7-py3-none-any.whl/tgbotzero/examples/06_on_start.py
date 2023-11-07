from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return 'Да-да, привет!'


def on_command_start(cmd: str):
    """Показать значение"""
    return 'Наш бот приветствует тебя, о великий сетевой путник!'


run_bot()
