from tgbotzero import *
TOKEN = '123:tokenHereFromBotFatherInTelegram'

def on_message(msg: str):
    # Проверяем, содержит ли сообщение два числа, разделённые знаком "+"
    if '+' in msg:
        numbers = msg.split('+')
        if len(numbers) == 2:
            try:
                # Пробуем преобразовать строки в числа и сложить
                num1 = float(numbers[0].strip())
                num2 = float(numbers[1].strip())
                result = num1 + num2
                return f"Результат: {result}"
            except ValueError:
                # Если преобразование не удалось, сообщаем об ошибке
                return "Пожалуйста, введите правильный пример на сложение (например, 2+2)."
    return "Отправьте пример на сложение (например, 2+2), и я верну результат."

run_bot()
