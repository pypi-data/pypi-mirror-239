from typing import Union, Tuple, Optional

import telebot

from tgbotzero.utils.reply_markup import Button, to_reply_markup

from tgbotzero.utils.images import Image, _image_manager


def send_answer(
        bot: telebot.TeleBot,
        chat_id: int,
        answer: Union[str, Button, Image, list[Union[str, Button, Image]]],
):
    texts = []
    buttons = []
    images = []

    if isinstance(answer, Button):
        buttons.append(answer)
    elif isinstance(answer, Image):
        images.append(answer)
    elif isinstance(answer, (list, tuple)):
        for obj in answer:
            if isinstance(obj, Button):
                buttons.append(obj)
            elif isinstance(obj, Image):
                images.append(obj)
            else:
                texts.append(str(obj))
    else:
        texts.append(str(answer))

    text = '\n'.join(texts) or '...'
    reply_markup = to_reply_markup(buttons)

    if len(images) > 1:
        media = [
            telebot.types.InputMediaPhoto(_image_manager[image] or image._io)
            for image in images
        ]
        megia_message = bot.send_media_group(chat_id, media=media)
        for image, message in zip(images, megia_message):
            file_id = message.photo[-1].file_id  # photo is an array of different sizes; [-1] gets the largest.
            _image_manager[image] = file_id
        bot.send_message(chat_id, text, reply_markup=reply_markup)
    elif len(images) == 1:
        image = images[0]
        photo = _image_manager[image] or image._io
        message = bot.send_photo(chat_id, photo=photo, caption=text, reply_markup=reply_markup)
        file_id = message.photo[-1].file_id  # photo is an array of different sizes; [-1] gets the largest.
        _image_manager[images[0]] = file_id
    else:
        bot.send_message(chat_id, text, reply_markup=reply_markup)
