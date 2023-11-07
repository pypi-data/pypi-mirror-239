import os
import sys
import atexit
import traceback
import types
import json
import re
from io import BytesIO
from typing import Union, Tuple, Optional

import PIL.Image
import requests
import telebot
import telebot.types

from tgbotzero.utils.help import help
from tgbotzero.utils.images import Image, _image_manager
from tgbotzero.utils.reply_markup import Button
from tgbotzero.utils.send_answer import send_answer
from tgbotzero.utils.check_on_button_functions import check_on_button_functions

bot = telebot.TeleBot('123:tokenHereFromBotFatherInTelegram')
already_started = False
main_module: Optional[types.ModuleType] = None


def handle_all_messages(message: telebot.types.Message):
    bot.send_message(message.chat.id, "BotZero работает только с текстовыми сообщениями.")


def set_up_token(bot: telebot.TeleBot, main_module: types.ModuleType):
    token = getattr(main_module, "TOKEN", None)
    if not token or 'BotFather' in token:
        token = os.environ.get('TOKEN', None)
    if not token:
        help()
        raise ValueError('Необходимо в переменную TOKEN записать токен телеграм-бота. Как-то так: '
                         'TOKEN = "123123123:abcabcabcabcabcabcabcabcabc"')
    bot.token = token


def set_up_on_text_message(bot: telebot.TeleBot, main_module: types.ModuleType):
    on_message = getattr(main_module, "on_message", None)
    if not on_message:
        help()
        raise ValueError('Необходимо определить функцию on_message. Например, так:'
                         'def on_message(msg: str):'
                         '    return "Твоё сообщение: " + msg')

    def on_text_message(message: telebot.types.Message):
        try:
            answer = on_message(message.text)
        except Exception as e:
            bot.send_message(message.from_user.id, f'Возникла ошибка:\n{traceback.format_exc()}')
            raise
        send_answer(bot, message.from_user.id, answer)

    bot.message_handler(content_types=['text'])(on_text_message)


def set_up_on_image_message(bot: telebot.TeleBot, main_module: types.ModuleType):
    on_image = getattr(main_module, "on_image", None)
    if not on_image:
        def on_image_message(message: telebot.types.Message):
            text = ('Необходимо определить функцию on_image. Например, так:'
                    'def on_image(msg: txt, img: Image):'
                    '    return ["Твоё фото", img]')
            bot.send_message(message.from_user.id, text)
            raise ValueError(text)
    else:
        def on_image_message(message: telebot.types.Message):
            try:
                file_id = message.photo[-1].file_id
                file_info = bot.get_file(file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                image = Image(downloaded_file)
                _image_manager[image] = file_id
                answer = on_image(message.caption or '', image)
            except Exception as e:
                bot.send_message(message.from_user.id, f'Возникла ошибка:\n{traceback.format_exc()}')
                raise
            send_answer(bot, message.from_user.id, answer)

    bot.message_handler(content_types=['photo'])(on_image_message)


def set_up_default_handler(bot: telebot.TeleBot, main_module: types.ModuleType):
    bot.message_handler(func=lambda message: True)(handle_all_messages)


def print_bot_info(bot: telebot.TeleBot):
    bot_info = bot.get_me()
    bot_name = bot_info.username

    print('Бот ждёт: https://t.me/' + bot_name)


@bot.message_handler(regexp="^/")
def handle_all_commands(message: telebot.types.Message):
    cmd = re.search(r'(?<=\/)[a-zA-Z_]*', message.text).group()
    if cmd == 'start':
        try:
            set_chat_commands(bot.token, bot.commands, message.from_user.id)
        except:
            pass
    command_function_name = f'on_command_{cmd}'
    command_function = getattr(main_module, command_function_name, None)
    if not command_function and cmd == 'start':
        command_function = default_on_start
    raise_exc = None
    if not command_function:
        answer = (f"Необходимо определить функцию {command_function_name}. Например:\n"
                  f"def {command_function_name}(cmd: str):\n"
                  f"    return 'Выполнена команда {cmd}, данные: ' + repr(cmd)\n")
        raise_exc = ValueError(answer)
    else:
        try:
            answer = command_function(message.text)
        except Exception as e:
            answer = f'Возникла ошибка:\n{traceback.format_exc()}'
            raise_exc = e
    send_answer(bot, message.from_user.id, answer)
    if raise_exc:
        raise raise_exc


def default_on_start(cmd: str):
    return 'Начинаем!'


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(callback_obj: telebot.types.CallbackQuery):
    name, data = callback_obj.data.split(";", maxsplit=1)
    data = json.loads(data)
    callback_function_name = f'on_button_{name}'
    callback_function = getattr(main_module, callback_function_name, None)
    raise_exc = None
    if not callback_function:
        answer = (f"Необходимо определить функцию {callback_function_name}. Например:\n"
                  f"def {callback_function_name}(data):\n"
                  f"    return 'Нажата кнопка {name}, данные: ' + repr(data)\n")
        raise_exc = ValueError(answer)
    else:
        try:
            answer = callback_function(data)
        except Exception as e:
            answer = f'Возникла ошибка:\n{traceback.format_exc()}'
            raise_exc = e

    bot.edit_message_reply_markup(chat_id=callback_obj.message.chat.id,
                                  message_id=callback_obj.message.message_id,
                                  reply_markup=None)
    raise_exc = send_answer(bot, callback_obj.from_user.id, answer) or raise_exc
    bot.answer_callback_query(callback_query_id=callback_obj.id)
    if raise_exc:
        raise raise_exc


def set_chat_commands(token, commands, chat_id):
    method_url = f"https://api.telegram.org/bot{token}/setMyCommands"
    payload = {
        "commands": commands,
        "scope": {
            "type": "chat",
            "chat_id": chat_id
        }
    }
    response = requests.post(method_url, json=payload)


def find_command_handlers(main_module):
    commands = []
    for attr_name in dir(main_module):
        if attr_name.startswith('on_command_'):
            attr = getattr(main_module, attr_name)
            if callable(attr):
                command = attr_name[len('on_command_'):]
                description = attr.__doc__ or command
                commands.append({"command": command, "description": description})
    return commands


def run_bot():
    global already_started
    if already_started:
        return
    already_started = True

    global main_module
    main_module = sys.modules["__main__"]

    set_up_token(bot, main_module)
    set_up_on_text_message(bot, main_module)
    set_up_on_image_message(bot, main_module)
    set_up_default_handler(bot, main_module)
    check_on_button_functions(main_module)
    bot.commands = find_command_handlers(main_module)

    # Now we start polling
    print_bot_info(bot)
    bot.infinity_polling()


def check_run_bot():
    if already_started:
        return
    raise ValueError('Необходимо добавить функцию run_bot() в конец кода для запуска бота')


if __name__ == '__main__':
    print('Модуль должен быть импортирован:\nfrom tgbotzero import *')
    sys.exit()

atexit.register(check_run_bot)
