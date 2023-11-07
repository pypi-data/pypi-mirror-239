<p align="center">
<a href="https://pypi.org/project/tgbotzero/" target="_blank">
<img alt="PyPI" src="https://img.shields.io/pypi/v/tgbotzero">
</a>
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/tgbotzero">
<img alt="GitHub" src="https://img.shields.io/github/license/ShashkovS/tgbotzero">
</p>

# TgBotZero

Телеграм-боты в пару строчек кода.
Простые телеграм-боты должно быть очень просто делать!

## Примеры

### Бот, показывающий твоё сообщение:

Для обработки текстовых сообщений нужно создать функцию `on_message(msg: str)`. Функция принимает текст сообщения, и может вернуть либо строку с текстом ответа, либо список из сообщений, описаний кнопок и картинок. Про кнопки и картинки будет дальше.


``` python
import tgbotzero

TOKEN = '123123123:tokenFromBotFatherInTelegram'

def on_message(msg: str):
    return "Твоё сообщение: " + msg
    
run_bot()
```

<img alt="echobot" src="https://github.com/ShashkovS/tgbotzero/raw/main/docs/echobot.png" width="417">


# Установка

Введите в терминале:

```shell
pip install tgbotzero --upgrade --user
```

Или запустите эту программу:

```python
import os, sys

python = sys.executable
user = '--user' if 'venv' not in python and 'envs' not in python else ''
cmd = f'"{python}" -m pip install tgbotzero --upgrade {user}'
os.system(cmd)
```



### Бот с кнопками:


Для того чтобы добавить к любому сообщению кнопку, нужно в список артефактов ответа добавить кнопки: `Button(text_on_button, button_handler_suffix, callback_data)`. Для обработки нажатий на кнопку нужно реализовать функцию `on_button_NAME(data)`, где `NAME=button_handler_suffix`. В качестве data будет передано `callback_data`.


``` python
from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'

def on_message(msg: str):
    return [
        "Твоё сообщение: " + msg,
        Button('Кнопка', 'btn'),
    ]

def on_button_btn(data):
    return 'Нажата кнопка. Отправьте любое сообщение для продолжения'

run_bot()
```

<img alt="echobot" src="https://github.com/ShashkovS/tgbotzero/raw/main/docs/buttonbot.png" width="600">

### Бот с командами:

Чтобы обрабатывать команды, нужно создать функцию вида `on_command_NAME(cmd: str)`, где `NAME` — это собственно команда. Например, для обработки команд `/start` нужна функция `on_command_start`. Функция может возвращать текст, кнопки и т.п. точно так же, как и `on_message` и другие хендлеры-обработчики. При вызове команды `/start` все команды будут автоматом добавлены в меню пользователя. Для указания описания команды функции нужно указать doc-string:
```python
def on_command_plus(cmd: str):
    """Add 1 to counter"""
```

```python
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
```

<img alt="commands" src="https://github.com/ShashkovS/tgbotzero/blob/main/docs/commands.png?raw=true" width="345">

### Бот с картинками:

Для отправки изображения нужно добавить в возвращаемый список `Image(image_filename)`. Можно отправлять несколько изображений в одном сообщении, в том числе отправлять изображения из обработчиков кнопок и команд.

```python
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
```
<img alt="gallery" src="https://github.com/ShashkovS/tgbotzero/blob/main/docs/gallery.png?raw=true" width="659">


### Обработка и модификация картинок:

Для обработки сообщений с картинками нужно создать функцию `on_image(msg: str, img: Image)`.
Изображения можно модифицировать. На данный момент поддерживается только добавление текста. Синтаксис: `img.put_text(text, color)`, где`color` — это RGB-кортеж, например, `(255, 0, 0)`. Изображения можно модифицировать даже если они открыты из файла: `Image(image_filename).put_text(text, color)`

```python
from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'

def on_message(msg: str):
    return 'Жду картинку с подписью!'

def on_image(msg: str, img: Image):
    return img.put_text(msg, (255, 0, 0))

run_bot()
```
<img alt="puttext" src="https://github.com/ShashkovS/tgbotzero/blob/main/docs/puttext.png?raw=true" width="323">



# [Contributing](CONTRIBUTING.md) 
