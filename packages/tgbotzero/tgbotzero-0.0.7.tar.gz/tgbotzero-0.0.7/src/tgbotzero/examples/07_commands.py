from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str):
    return '''Доступны команды:
/show — показать
/plus — прибавить 1
/minus — вычесть 1'''


counter = 0


def on_command_show(cmd: str):
    """Показать значение"""
    return f'{counter=}'


def on_command_plus(cmd: str):
    """Прибавить 1"""
    global counter
    counter += 1
    return f'{counter=}'


def on_command_minus(cmd: str):
    """Вычесть 1"""
    global counter
    counter -= 1
    return f'{counter=}'


run_bot()
