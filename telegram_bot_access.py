import telebot
from telebot import types
import cities_data

# создаём бота по токену
bot = telebot.TeleBot('8187783775:AAFv7bQa8CK5FkX3PP-0b5plYmxFlYCEV6g')


# делаем обработчик сообщений
@bot.message_handler(content_types=['text'])
def start_chatting(message):
    # приветственное сообщение (оно же и при перезапуске)
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Привет, готов начать?")
        bot.register_next_step_handler(message, choose_game)


# выбор игры пользователем
def choose_game(message):
    # создаём клавиатуру - выбор игры с небольшим интерфейсом
    keyboard = types.InlineKeyboardMarkup()
    # Создаём клавишу судоку
    key_sudoku = types.InlineKeyboardButton(text='Судоку', callback_data='sudoku')
    # Добавляем кнопку с судоку на клавиатуру
    keyboard.add(key_sudoku)
    # Создаём клавишу города
    key_cities = types.InlineKeyboardButton(text='Города', callback_data='cities')
    # Добавляем клавишу города на клавиатуру
    keyboard.add(key_cities)
    bot.send_message(message.from_user.id, text="В какую игру вы бы хотели сегодня поиграть?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "cities":
        bot.send_message(call.message.chat.id, 'Города')
    else:
        bot.send_message(call.message.chat.id, 'Судоку')


# Запускаем работу бота
bot.polling(none_stop=True, interval=0)
