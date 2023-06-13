import sys

import telebot
import requests
import time
import threading
import subprocess

from telebot import types
from requests import get
from datetime import datetime

from google_calendar import radio_scheduler

# Load variables data from the config file
from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_VOICE_CHAT_LINK,
    TELEGRAM_VOICE_CHAT_KEY,
    STREAM_URL,
    STREAM_STATUS,
    ADMINS,
    SUPPORT
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)  # variable to provide Telegram bot token to the Telebot
stream_process = None  # variable to store the stream process
stream_command = ['ffmpeg', '-stream_loop', '-1', '-re', '-i', STREAM_URL,
                  '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k',
                  '-f', 'flv', '-flvflags', 'no_duration_filesize',
                  TELEGRAM_VOICE_CHAT_LINK + TELEGRAM_VOICE_CHAT_KEY]


# Function to create the formatted timestamp
def timestamp():
    current_time = datetime.now()  # variable to get current date
    green = '\033[92m'  # ANSI escape sequence for green color text
    reset = '\033[0m'  # ANSI escape sequence to reset text color
    timestamp_formatted = f'{green}{current_time.strftime("%Y-%m-%d %H:%M:%S")}{reset}\n-------------------\n'
    return f'\n\n{timestamp_formatted}'


# Function to update the log file
def logging(error):
    sys.stderr.write(error)
    with open('/var/log/telegram-bot.log', 'a') as file:
        file.write(f'\n{timestamp()}'
                   f'{error}')


# Function to check stream URL is available
def stream_url_status():
    attempt = 1
    while attempt < 6:
        response = requests.get(STREAM_URL, stream=True)
        if response:
            print(f'attempt {attempt}:\n'
                  f'----------\n'
                  f'=> URL: {STREAM_URL}\n'
                  f'=> Response: {response.status_code}\n')
            return True
        else:
            print(f'attempt {attempt}:\n'
                  f'----------\n'
                  f'=> URL: {STREAM_URL}\n'
                  f'=> Response: {response.status_code}\n')
            time.sleep(5)
            attempt += 1
    return False


# Function to play the stream
def stream_play():
    global stream_process
    if stream_process is None:
        print(f'{timestamp()}'
              f'=> Starting the stream process...\n'
              f'=> Command: {" ".join(stream_command)}\n')
        stream_process = subprocess.Popen(stream_command,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          universal_newlines=True)
        output, error = stream_process.communicate()
        stream_error(error)


# Function to stop the stream
def stream_stop():
    global stream_process
    print(f'\n{timestamp()}'
          f'=> Stopping the stream process...\n')
    if stream_process is not None:
        stream_process.terminate()
        stream_process.wait()
        stream_process = None
        print('\n=> Stream stopped!\n')


# Function to restart the stream
def stream_restart():
    global stream_process
    print(f'{timestamp()}'
          f'=> Restarting the stream process...\n')
    stream_process.terminate()
    stream_process.wait()
    stream_process = None
    stream_thread = threading.Thread(target=stream_play)
    stream_thread.start()


# Function to parse the output for the known errors
def stream_error(error):
    if "Function not implemented" in error:
        print(f'\n{timestamp()}'
              f'=> ERROR: connection to the Icecast2 server interrupted.\n')
        logging(error)
        time.sleep(15)
        stream_restart()
    elif "I/O error" and "Failed to resolve hostname" in error:
        print(f'\n{timestamp()}'
              f'=> ERROR: connection to the Icecast2 server failed.\n')
        logging(error)
        time.sleep(15)
        stream_restart()
    elif "Conversion failed!" in error:
        print(f'\n{timestamp()}'
              f'=> ERROR: ffmpeg conversion failed.\n')
        logging(error)
        time.sleep(15)
        stream_restart()
    elif "I/O error" and "Error opening output rtmps" in error:
        print(f'\n{timestamp()}'
              f'=> ERROR: voice chat in the Telegram group is busy.\n')
        logging(error)
        time.sleep(30)
        stream_restart()
    elif "Error" or "error" or "Failed" or "failed" in error:
        print(f'\n{timestamp()}'
              f'=> ERROR: unknown error - check the logs.\n')
        logging(error)
        time.sleep(30)
        stream_restart()


# Function to parse the current song
def get_song():
    resp = get(STREAM_STATUS).json()
    return resp.get("icestats").get("source").get("title")


# Function to get the chat ID for a given username
def get_chat_id(username):
    try:
        user_info = bot.get_chat(username)
        return user_info.id
    except telebot.apihelper.ApiTelegramException:
        return None


# Function to send the report to support
def report_process(message):
    report_text = message.text
    # Send the report to support users (SUPPORT only)
    for username in SUPPORT:
        support_chat_id = get_chat_id(username)
        if support_chat_id:
            bot.send_message(support_chat_id,
                             f'Сообщение от пользователя\n'
                             f'=========================\n'
                             f'Username: {message.from_user.username}\n'
                             f'ID: {message.from_user.id}\n'
                             f'=========================\n'
                             f'{report_text}')
        else:
            bot.reply_to(message, f'🚫 Ошибка отправки сообщения пользователю {username}!\n')
    # Send a confirmation message to the user
    bot.reply_to(message, '👍🏻 Спасибо!\nВаш запрос отправлен в службу поддержки.')


# Handler for the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == 'private':  # check the chat is private
        # Send a photo along with the start command response
        photo_url = 'https://radio.daomars.net/wp-content/uploads/2023/05/flood-morning-300x300.png'
        bot.send_photo(message.chat.id, photo_url, caption='Добро пожаловть в бота MarsDAO Radio!')
        handle_menu(message)  # Call the handle_menu function to show the menu message and buttons
    else:
        # Skip execution for the non-private chats and remove the command message
        bot.delete_message(message.chat.id, message.message_id)


# Handler for the /play command
@bot.message_handler(commands=['play'])
# Handler for the Play button (ADMINS only)
@bot.message_handler(func=lambda message: message.text == '▶️ Play')
def handle_play(message):
    if message.chat.type == 'private':  # check the chat is private
        if message.from_user.id in ADMINS:
            if stream_process is not None:
                bot.send_message(message.chat.id, '🚫 Ошибка!\nВещание радиостанции в Telegram уже запущено!')
            else:
                bot.reply_to(message, '▶️ Запуск вещания ридостанции в Telegram...')
                stream = threading.Thread(target=stream_play)
                stream.start()
        else:
            bot.reply_to(message, '🚫 Ошибка!\nУ вас не достаточно прав для использования этой команды.')
    else:
        # Skip execution for the non-private chats and remove the command message
        bot.delete_message(message.chat.id, message.message_id)


# Handler for the /stop command
@bot.message_handler(commands=['stop'])
# Handler for the Stop button (ADMINS only)
@bot.message_handler(func=lambda message: message.text == '⏹️ Stop')
def handle_stop(message):
    if message.chat.type == 'private':  # check the chat is private
        if message.from_user.id in ADMINS:
            bot.reply_to(message, '⏹️ Остановка вещания ридостанции в Telegram...')
            stream_stop()
        else:
            bot.reply_to(message, '🚫 Ошибка!\nУ вас не достаточно прав для использования этой команды.')
    else:
        # Skip execution for the non-private chats and remove the command message
        bot.delete_message(message.chat.id, message.message_id)


# Handler for the /restart command
@bot.message_handler(commands=['restart'])
# Handler for the Restart button (ADMINS only)
@bot.message_handler(func=lambda message: message.text == '🔄 Restart')
def handle_restart(message):
    if message.chat.type == 'private':  # check the chat is private
        if message.from_user.id in ADMINS:
            bot.reply_to(message, '🔄 Перезапуск вещания ридостанции в Telegram...')
            stream_restart()
        else:
            bot.reply_to(message, '🚫 Ошибка!\nУ вас не достаточно прав для использования этой команды.')
    else:
        # Skip execution for the non-private chats and remove the command message
        bot.delete_message(message.chat.id, message.message_id)


# Handler for the /status command
@bot.message_handler(commands=['status'])
# Handler for the Restart button (ADMINS only)
@bot.message_handler(func=lambda message: message.text == 'ℹ️ Status')
def handle_status(message):
    if message.chat.type == 'private':  # check the chat is private
        global stream_process
        if stream_process is not None:
            bot.send_message(message.chat.id, 'ℹ️ Вещание ридостанции в Telegram работает!')
        else:
            bot.send_message(message.chat.id, '🚫 Вещание ридостанции в Telegram НЕ работает!')
    else:
        # Skip execution for the non-private chats and remove the command message
        bot.delete_message(message.chat.id, message.message_id)


# Handler for the /song command
@bot.message_handler(commands=['song'])
# Handler for the Song button
@bot.message_handler(func=lambda message: message.text == '🎶 Song')
def handle_song(message):
    if message.chat.type == 'private':  # check the chat is private
        bot.reply_to(message, f'🎶 Сейчас играет:\n{get_song()}')
    else:
        song_text = f'🎶 Сейчас играет:\n{get_song()}'
        bot.send_message(message.chat.id, song_text)
        bot.delete_message(message.chat.id, message.message_id)


# Handler for the /report command
@bot.message_handler(commands=['report'])
# Handler for the Report button
@bot.message_handler(func=lambda message: message.text == '💬 Report')
def handle_report(message):
    if message.chat.type == 'private':  # check the chat is private
        # Create the cancel button
        markup = types.InlineKeyboardMarkup()
        cancel_button = types.InlineKeyboardButton('🚫 Cancel', callback_data='cancel_report')
        markup.add(cancel_button)

        # Send a prompt message to the user with the cancel button
        prompt_message = 'Пожалуйста введите своё сообщение для службы поддержки или нажмите кнопку отмены для прекращения этого действия:'
        bot.send_message(message.chat.id, prompt_message, reply_markup=markup)

        # Register the next message handler to listen for the report
        bot.register_next_step_handler(message, report_process)
    else:
        # Skip execution for the non-private chats and remove the command message
        bot.delete_message(message.chat.id, message.message_id)


# Handler for processing callback from the cancel button
@bot.callback_query_handler(func=lambda call: call.data == 'cancel_report')
def handle_cancel_report(call):
    # Send a message in the chat that the report has been cancelled
    bot.send_message(call.message.chat.id, '🚫 Ваше сообщение в службу поддержки отменено.')

    # Delete the original message with the report
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Clear the next step handler for the current chat
    bot.clear_step_handler_by_chat_id(call.message.chat.id)


# Handler for the /help command
@bot.message_handler(commands=['help'])
# Handler for the Help button
@bot.message_handler(func=lambda message: message.text == '❓ Help')
def handle_help(message):
    if message.chat.type == 'private':  # check the chat is private
        help_text = '''
Это раздел помощи бота MarsDAO Radio.

Группа радиостанции: https://t.me/MarsDAO_radio
Сайт радиостанции: https://radio.daomars.net

Доступные следующие команды:
/start - Запустить бота
/play - Запустить вещание радиостанции в Telegram (только для администраторов)
/stop - Остановить вещание радиостанции в Telegram (только для администраторов)
/restart - Перезапустить вещание радиостанции в Telegram (только для администраторов)
/status - Статус вещания радиостанции в Telegram
/scheduler - Показать расписание сетки вещания радиостанции на текущую неделю
/song - Получить название текущей композиции в эфире
/report - Отправить сообщение в службу поддержки
/help - Показать это сообщение справки

Вы также можете использовать кнопки меню ниже для управления ботом.
    '''
        bot.reply_to(message, help_text)
    else:
        # Skip execution for the non-private chats and remove the command message
        bot.delete_message(message.chat.id, message.message_id)


# Handler for the /scheduler command
@bot.message_handler(commands=['scheduler'])
# Handler for the Help button
@bot.message_handler(func=lambda message: message.text == '📆 Scheduler')
def handle_help(message):
    if message.chat.type == 'private':  # check the chat is private
        scheduler_text = radio_scheduler()
        if scheduler_text:
            bot.reply_to(message, scheduler_text)
        else:
            bot.reply_to(message, '🚫 Ошибка!\nИнформация об расписании сетки вещания радиостанции не доступна.')
    else:
        # Skip execution for the non-private chats and remove the command message
        bot.delete_message(message.chat.id, message.message_id)


# Handler for the main menu
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.chat.type == 'private':  # check the chat is private
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if message.from_user.id in ADMINS:
            button_play = types.InlineKeyboardButton('▶️ Play')
            button_stop = types.InlineKeyboardButton('⏹️ Stop')
            button_restart = types.InlineKeyboardButton('🔄 Restart')
            markup.row(button_play, button_stop)
            markup.row(button_restart)
        button_song = types.InlineKeyboardButton('🎶 Song')
        button_scheduler = types.InlineKeyboardButton('📆 Scheduler')
        markup.row(button_song, button_scheduler)
        button_status = types.InlineKeyboardButton('ℹ️ Status')
        button_report = types.InlineKeyboardButton('💬 Report')
        button_help = types.InlineKeyboardButton('❓ Help')
        markup.row(button_status, button_report, button_help)
        bot.send_message(message.chat.id, 'Выберите вариант из меню, чтобы продолжить пользоваться ботом MarsDAO Radio 👇🏻',
                         reply_markup=markup)


# Start the bot
def main():
    print(f'\n\n\n===============================\n'
          f'MarsDAO Radio bot version 1.3.0'
          f'\n===============================\n\n'
          f'Source: https://github.com/profinch/telegram-bot-icecast-radio'
          f'{timestamp()}'
          f'=> Checking the stream URL...\n')
    if stream_url_status():
        print('=> The stream URL is available.')
    else:
        print(f'{timestamp()}'
              f'=> ERROR: Stream URL is not available!\n'
              f'=> Bye!')
        quit()
    try:
        print('\n=> Starting the stream in...')
        for i in range(3, 0, -1):
            print(f'=> {i} seconds')
            time.sleep(1)
        stream = threading.Thread(target=stream_play)
        stream.start()
        time.sleep(1)
        print('=> Starting the bot polling...\n')
        bot.polling(none_stop=True, timeout=60)
    except Exception as error_polling:
        print(f'\n{timestamp()}'
              f'\n=> An error occurred while polling:', str(error_polling))
        print(f'\n=> Bye!\n')
        quit()


if __name__ == '__main__':
    main()
