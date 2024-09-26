# Бот-ассистент.

## Описание
Telegram-бота, который будет обращаться к API сервиса Практикум.Домашка и узнавать статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Возможности:
* раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы;
* при обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram;
* логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.

## Инструкция

1. **Клонируйте репозиторий:**

   ```bash
   git clone git@github.com:Elijah-iSO/homework_bot.git
   cd homework_bot
   ```
2. **Создание и активация окружения:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
3. **Обновление pip и установка зависимостей:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Создайте файл `.env`:**

   ```bash
   touch .env
   ```

   **Добавьте следующие переменные в  `.env`:**

   ```
   PRACTICUM_TOKEN=<TOKEN_API>
   TELEGRAM_TOKEN=<ВАШ_ТОКЕН_ТЕЛЕГРАМ>
   TELEGRAM_CHAT_ID=<ВАШ_ID_ЧАТА_ТЕЛЕГРАМ>
   ```

5. **Запустите проект:**

   ```bash
   python3 main.py
   ```

## Cтек технологий
<span style="display: inline-block; margin-right: 5px;">[![Python](https://img.shields.io/badge/python-3.9-blue)](https://www.python.org/)</span>
<span style="display: inline-block; margin-right: 5px;">[![Logging](https://img.shields.io/badge/logging-python-yellow)](https://docs.python.org/3/library/logging.html)</span>
<span style="display: inline-block; margin-right: 5px;">[![Pytest](https://img.shields.io/badge/pytest-6.2.5-red)](https://docs.pytest.org/en/latest/)</span>
<span style="display: inline-block; margin-right: 5px;">[![Pytest Timeout](https://img.shields.io/badge/pytest--timeout-2.1.0-yellowgreen)](https://pypi.org/project/pytest-timeout/)</span>
<span style="display: inline-block; margin-right: 5px;">[![Python Dotenv](https://img.shields.io/badge/python--dotenv-0.19.0-blue)](https://pypi.org/project/python-dotenv/)</span>
<span style="display: inline-block; margin-right: 5px;">[![Python Telegram Bot](https://img.shields.io/badge/python--telegram--bot-13.7-blueviolet)](https://github.com/python-telegram-bot/python-telegram-bot)</span>
<span style="display: inline-block; margin-right: 5px;">[![Requests](https://img.shields.io/badge/requests-2.26.0-green)](https://docs.python-requests.org/en/master/)</span> 

## Автор
ILYA OLEYNIKOV
GitHub:	https://github.com/Elijah-iSO
E-mail: oleynikovis@yandex.ru
