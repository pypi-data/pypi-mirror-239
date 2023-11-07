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

``` python
import tgbotzero

TOKEN = '123123123:tokenFromBotFatherInTelegram'

def on_message(msg: str):
    return "Твоё сообщение: " + msg
```

<img alt="echobot" src="https://github.com/ShashkovS/tgbotzero/raw/main/docs/echobot.png" width="417">

### Бот с кнопками:

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

# [Contributing](CONTRIBUTING.md) 
