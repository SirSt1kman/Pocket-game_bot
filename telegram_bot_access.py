import telebot
from cities_game import cities_loop, choose_random_city, new_game

# создаём бота по токену
bot = telebot.TeleBot('8187783775:AAFv7bQa8CK5FkX3PP-0b5plYmxFlYCEV6g')
bot.remove_webhook()


def last_char_search(word: str) -> str:
    """Функция, ищущая последнюю букву города, кроме ё, ы, ъ, ь"""

    while word[-1] in 'ёыьъ':
        word = word[:-1]
    return word[-1]


@bot.message_handler(content_types=['text'])
def start(message):
    """Приветствие пользователя"""

    # приветственное сообщение (оно же и при перезапуске бота)
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Привет, я бот Судода Гороку")

    # выбор игры и ветки для игр судоку и города
    if (not cities_branch) and (not sudoku_branch):
        choose_game(message)
    if cities_branch:
        cities_game(message)
    elif sudoku_branch:
        pass


def choose_game(message):
    """Выбор игры в боте"""
    global cities_branch, sudoku_branch

    # города
    if message.text.lower() == 'города':
        cities_branch = True
        sudoku_branch = False
        bot.send_message(message.from_user.id, "Играем в города, поехали!")
        bot.send_message(message.from_user.id, "Правила игры:"
                                               "* Каждый город должен входить в число городов России"
                                               "* Нельзя дважды повторять один и тот же город"
                                               "* Называть город можно только на последнюю букву предыдущего города"
                                               "* Последней буквой считаются все, кроме ё, ъ, ы, ь"
                                               "* Регистр учитывается, пишите с маленькой буквы"
                                               "* Побеждает тот, кто последним назовёт город из списка"
                                               "* Чтобы вернуться к выбору игр напишите выход"
                                               "* Чтобы снова сыграть в города напишите play")

    # судоку
    if message.text.lower() == 'судоку':
        sudoku_branch = True
        cities_branch = False
        bot.send_message(message.from_user.id, "Играем в судоку, погнали!")

    if message.text == '/start':
        bot.send_message(message.from_user.id, "В какую игру ты хочешь поиграть, судоку или города?")
        bot.send_message(message.from_user.id, "Если судоку, то напиши судоку, если города - города.")


@bot.message_handler(content_types=['text'])
def cities_game(message):
    """Функция, основное тело игры"""
    global bot_says, flag_0, cities_branch

    # то, что мы написали
    text = message.text.lower()
    if text != 'города':
        # переменная, хранящая значение функции о проверке города в начале игры
        if bot_says == '':
            verdict = cities_loop(text, '1', bool(flag_0))
        else:
            last_char = last_char_search(bot_says)
            verdict = cities_loop(text, last_char, bool(flag_0))

        # Было принято решение вернуться назад в меню
        if verdict == 'exit':
            cities_branch = False
            bot.send_message(message.from_user.id, "Заглядывай поиграть со мной позже, буду ждать.")
            start(message)

        # играть ещё раз
        if verdict == 'play':
            bot.send_message(message.from_user.id, "Играем снова, начинай!")
            bot_says = ''
            flag_0 = 1
            new_game()
            start(message)

        # Игра уже окончена
        if verdict == 'game over':
            bot.send_message(message.from_user.id, "Мы уже сыграли, разве нет? "
                                                   "Ты можешь начать игру ещё раз, если хочешь. Для этого пиши play.")

        # Был введён не город, а другое слово
        if verdict == 'not city':
            bot.send_message(message.from_user.id, "Извини, но мы играем в города, а не просто слова. "
                                                   "Попробуй назвать город.")

        # Был назван город, который уже упоминался в игре
        if verdict == 'repeat':
            bot.send_message(message.from_user.id, "Прости, в городах нельзя повторяться, нельзя. "
                                                   "Вспомни другой город.")

        # Был назван город, но не на нужную букву
        if verdict == 'wrong input':
            bot.send_message(message.from_user.id, "Нет, тебе следует называть город на ту букву, "
                                                    "на которую оканчивается мой.")

        # Окончание игры в случае победы над ботом путем исключения всех слов из списка городов на одну букву
        if verdict == 'won by bot':
            flag_0 -= 1
            bot.send_message(message.from_user.id, "Ха-Ха, я тебя одолел! Бросишь мне вызов ещё раз?"
                                                   "Пиши play.")

        # Окончание игры в результате полной победы над ботом путем исключения всех городов из списка
        if verdict == 'totally won':
            flag_0 -= 1
            bot.send_message(message.from_user.id, "Это грандиозная победа! Тебе никогда меня не превзойти!"
                                                   "Хочешь ещё раз проиграть мне? Тогда напиши play")

        # Блок функции, выполняющийся при корректном вводе города
        if verdict == 'ok':
            # последняя буква города, на которую есть какие-либо города в России (не ё, ы, ъ, ь)
            last_char = last_char_search(text)
            # город, выбранный ботом
            new_city = choose_random_city(last_char)

            # проверка на проигрыш
            if new_city == 'bot lose':
                flag_0 -= 1
                bot.send_message(message.from_user.id, "Поздравляю, ты одолел меня! Я не смог вспомнить ни одного "
                                                       "подходящего слова. Если хочешь сыграть ещё раз, напиши play")
            else:
                bot_says = new_city
                bot.send_message(message.from_user.id, new_city)


bot_says = ''
flag_0 = 1
cities_branch = False
sudoku_branch = False
# Запускаем работу бота
bot.polling(none_stop=True, interval=0)
