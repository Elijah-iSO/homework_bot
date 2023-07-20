import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


def check_tokens():
    """Проверяет доступность переменных окружения.
    Если отсутствует хотя бы одна переменная окружения —
    продолжать работу бота нет смысла
    """
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат, определяемый переменной окружения.
    TELEGRAM_CHAT_ID. Принимает на вход два параметра:
    экземпляр класса Bot и строку с текстом сообщения.
    """
    try:
        bot.send_message(TELEGRAM_CHAT_ID, text=message)
        logger.debug(
            f'{message} успешно отправлено пользователю {TELEGRAM_CHAT_ID}')
    except Exception as error:
        logger.error(f'Бот не смог отправить сообщение, ошибка: {error}')


def get_api_answer(timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса.
    В качестве параметра в функцию передается временная метка.
    В случае успешного запроса должна вернуть ответ API,
    приведя его из формата JSON к типам данных Python.
    """
    payload = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(ENDPOINT,
                                         headers=HEADERS,
                                         params=payload)
        if homework_statuses.status_code == HTTPStatus.OK:
            return homework_statuses.json()
        else:
            raise requests.exceptions.RequestException()
    except requests.exceptions.RequestException:
        raise ConnectionError('Ошибка подключения')


def check_response(response):
    """Проверяет ответ API на соответствие документации из урока.
    API сервиса Практикум.Домашка. В качестве параметра функция получает
    ответ API, приведенный к типам данных Python.s
    """
    if not isinstance(response, dict):
        raise TypeError('responce должен быть словарем')
    if 'homeworks' not in response:
        raise KeyError('отсутствует ключ homeworks')

    homework = response['homeworks']
    if not isinstance(homework, list):
        raise TypeError('homework должен быть списком')

    current_date = response['current_date']
    if current_date is None:
        raise KeyError('отсутствует ключ homeworks')


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус этой работы.
    В качестве параметра функция получает только один элемент из списка
    домашних работ. В случае успеха, функция возвращает подготовленную для
    отправки в Telegram строку, содержащую один из вердиктов словаря
    HOMEWORK_VERDICTS.
    """
    status = homework.get('status')
    homework_name = homework.get('homework_name')
    if status not in HOMEWORK_VERDICTS:
        raise KeyError('статус работы отличается от возможных')
    else:
        verdict = HOMEWORK_VERDICTS[status]
    if 'homework_name' not in homework:
        raise KeyError('отсутствует ключ homework_name')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if check_tokens() is False:
        logger.critical('Отсутствует один из обязательных токенов.')
        sys.exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    last_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            timestamp = response.get('current_date')
            check_response(response)
            homework = response.get('homeworks')[0]

            message = parse_status(homework)
            if last_message != message:
                send_message(bot, message)
                last_message = message

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
