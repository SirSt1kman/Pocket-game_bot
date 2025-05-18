import telebot
from cities_game import cities_loop, choose_random_city, new_game
from sudoku_generator import sudoku_unsolved, sudoku_solved
from sudoku_game import sudoku_loop, new_game_sudoku

# создаём бота по токену
bot = telebot.TeleBot('8187783775:AAFv7bQa8CK5FkX3PP-0b5plYmxFlYCEV6g')
bot.remove_webhook()


def last_char_search(word: str) -> str:
    """Функция, ищущая последнюю букву города, кроме ё, ы, ъ, ь"""

    while word[-1] in 'ёыьъ':
        word = word[:-1]
    return word[-1]


def formatted_print(message, arr: list) -> None:
    """Функция, выводящая в чат-бот сетку судоку"""
    print_line = []
    for line in arr:
        for element in line:
            if element == 0:
                print_line.append('  ')
            else:
                print_line.append(str(element))
    bot.send_message(message.from_user.id, '{} | {} | {} | {} | {} | {} | {} | {} | {} \n-------------------------\n'
                                           '{} | {} | {} | {} | {} | {} | {} | {} | {} \n-------------------------\n'
                                           '{} | {} | {} | {} | {} | {} | {} | {} | {} \n-------------------------\n'
                                           '{} | {} | {} | {} | {} | {} | {} | {} | {} \n-------------------------\n'
                                           '{} | {} | {} | {} | {} | {} | {} | {} | {} \n-------------------------\n'
                                           '{} | {} | {} | {} | {} | {} | {} | {} | {} \n-------------------------\n'
                                           '{} | {} | {} | {} | {} | {} | {} | {} | {} \n-------------------------\n'
                                           '{} | {} | {} | {} | {} | {} | {} | {} | {} \n-------------------------\n'
                                           '{} | {} | {} | {} | {} | {} | {} | {} | {} \n'.format(*print_line))


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
        sudoku_game(message)


def choose_game(message):
    """Выбор игры в боте"""
    global cities_branch, sudoku_branch

    #Предупреждение о неправильно введённом кодовом слове
    if message.text.lower() not in ['/start', 'судоку', 'города', 'exit']:
        bot.send_message(message.from_user.id, "Простите, я не знаю такой команды")

    # города
    if message.text.lower() == 'города':
        cities_branch = True
        sudoku_branch = False
        cities_start()
        new_game()
        bot.send_message(message.from_user.id, "Играем в города, поехали!")
        bot.send_message(message.from_user.id, "Правила игры:\n"
                                               "* Каждый город должен входить в число городов России\n"
                                               "* Нельзя дважды повторять один и тот же город\n"
                                               "* Называть город можно только на последнюю букву предыдущего города\n"
                                               "* Последней буквой считаются все, кроме ё, ъ, ы, ь\n"
                                               "* Регистр не учитывается, пишите с любой буквы\n"
                                               "* Побеждает тот, кто последним назовёт город из списка\n"
                                               "* Чтобы вернуться к выбору игр напишите выход\n"
                                               "* Чтобы снова сыграть в города напишите play")

    # судоку
    if message.text.lower() == 'судоку':
        sudoku_branch = True
        cities_branch = False
        new_game_sudoku()
        bot.send_message(message.from_user.id, "Играем в судоку, погнали!")
        bot.send_message(message.from_user.id, "Правила игры:\n"
                                               "* Каждый столбец судоку должен содержать по одной цифре от 1 до 9\n"
                                               "* Каждая строка судоку должна содержать по одной цифре от 1 до 9\n"
                                               "* Каждый блок судоку 3 на 3 должен содержать по одной цифре от 1 до 9\n"
                                               "* Поражение засчитывается в случае, если игрок допустил 3 ошибки\n"
                                               "* Игрок побеждает, если всё поле судоку заполнено правильно\n"
                                               "* Чтобы поставить цифру в клетку, укажите через пробел её координаты "
                                               "по х и у (слева направо и сверху вниз от 1 до 9), а потом через пробел"
                                               "цифру, которую вы хотите поставить в соответствующую клетку\n"
                                               "* У вас есть три права на ошибку, после этого вы проигрываете\n"
                                               "* Чтобы вернуться к выбору игр напишите выход\n"
                                               "* Чтобы снова сыграть в города напишите play")
        formatted_print(message, sudoku_unsolved)

    # начальная ветка, перезапуск бота
    if message.text == '/start':
        bot.send_message(message.from_user.id, "В какую игру ты хочешь поиграть, судоку или города?")
        bot.send_message(message.from_user.id, "Если судоку, то напиши судоку, если города - города.")


def cities_start() -> None:
    """Начало игры в города"""
    global last_char, flag_0
    last_char = '1'
    flag_0 = True


def cities_game(message):
    """Функция, основное тело игры в города"""
    global last_char, flag_0, cities_branch

    # то, что мы написали
    text = message.text.lower()

    # играть ещё раз
    if text == 'play':
        cities_start()
        bot.send_message(message.from_user.id, "Играем сначала!")
        new_game()

    # выход из игры в города
    elif text == 'exit':
        cities_branch = False
        bot.send_message(message.from_user.id, "Заглядывай поиграть со мной позже, буду ждать.\n"
                                               "Напиши /start для перезапуска.")
        choose_game(message)

    elif text != 'города':
        # переменная, хранящая значение функции о проверке города в начале хода
        verdict = cities_loop(text, last_char, flag_0)

        # Игра уже окончена
        if verdict == 'game over':
            bot.send_message(message.from_user.id, "Мы уже сыграли, разве нет? "
                                                   "Ты можешь начать игру ещё раз, если хочешь. Для этого пиши play.")

        # Был введён не город, а другое слово
        elif verdict == 'not city':
            bot.send_message(message.from_user.id, "Извини, но мы играем в города, а не просто слова. "
                                                   "Попробуй назвать город.")

        # Был назван город, который уже упоминался в игре
        elif verdict == 'repeat':
            bot.send_message(message.from_user.id, "Прости, в городах нельзя повторяться, нельзя. "
                                                   "Вспомни другой город.")

        # Был назван город, но не на нужную букву
        elif verdict == 'wrong input':
            bot.send_message(message.from_user.id, "Нет, тебе следует называть город на ту букву, "
                                                    "на которую оканчивается мой.")

        # Окончание игры в случае победы над ботом путем исключения всех слов из списка городов на одну букву
        elif verdict == 'won by bot':
            flag_0 = False
            bot.send_message(message.from_user.id, "Ха-Ха, я тебя одолел! Бросишь мне вызов ещё раз?"
                                                   "Пиши play.")

        # Окончание игры в результате полной победы над ботом путем исключения всех городов из списка
        elif verdict == 'totally won':
            flag_0 = False
            bot.send_message(message.from_user.id, "Это грандиозная победа! Тебе никогда меня не превзойти!"
                                                   "Хочешь ещё раз проиграть мне? Тогда напиши play")

        # Блок функции, выполняющийся при корректном вводе города
        elif verdict == 'ok':
            # последняя буква города, на которую есть какие-либо города в России (не ё, ы, ъ, ь)
            last_char = last_char_search(text)
            # город, выбранный ботом
            new_city = choose_random_city(last_char)

            # проверка на проигрыш
            if new_city == 'bot lose':
                flag_0 = False
                bot.send_message(message.from_user.id, "Поздравляю, ты одолел меня! Я не смог вспомнить ни одного "
                                                       "подходящего слова. Если хочешь сыграть ещё раз, напиши play")
            else:
                last_char = last_char_search(new_city)
                bot.send_message(message.from_user.id, new_city.capitalize())


def sudoku_game(message):
    """Функция, основное тело игры в судоку"""
    global sudoku_branch, mistakes, f0, sudoku_solved, sudoku_unsolved

    # то, что мы написали
    text = message.text.lower()

    # играть ещё раз
    if text == 'play':
        mistakes = 0
        f0 = True
        sudoku_unsolved, sudoku_solved = new_game_sudoku()
        formatted_print(message, sudoku_unsolved)
        bot.send_message(message.from_user.id, "Играем сначала!")


    # выход из игры в города
    elif text == 'exit':
        sudoku_branch = False
        bot.send_message(message.from_user.id, "Заглядывай поиграть со мной позже, буду ждать.\n"
                                               "Напиши /start для перезапуска.")
        choose_game(message)

    elif text != 'судоку':
        # переменная, хранящая значение функции о проверке города в начале хода
        try:
            pos_x, pos_y, num = list(map(int, text.split()))
            verdict = sudoku_loop(pos_x, pos_y, num, mistakes, f0)

            if verdict == 'already played':
                bot.send_message(message.from_user.id, "Ты уже сыграл, разве нет?\n"
                                                       "Напиши play, чтобы сыграть ещё раз.")

            elif verdict == 'lose':
                bot.send_message(message.from_user.id, "Вы ошиблись трижды, хотите начать сначала?\n"
                                                       "Напишите play, чтобы перезапустить раскладку.")
                f0 = False

            elif verdict == 'wrong position':
                bot.send_message(message.from_user.id, "Вы неправильно указали координаты клетки.\n"
                                                       "Попробуйте ещё раз. Помните, что они от 1 до 9")

            elif verdict == 'wrong number':
                bot.send_message(message.from_user.id, "Вы неправильно указали значение клетки.\n"
                                                       "Попробуйте ещё раз.")

            elif verdict == 'already num':
                bot.send_message(message.from_user.id, "На этой позиции уже стоит цифра.\n"
                                                       "Выберите другую клетку.")

            elif verdict == 'mistake':
                mistakes += 1
                bot.send_message(message.from_user.id, "Будьте внимательней, вы ошиблись")

            elif verdict == 'ok':
                sudoku_unsolved[pos_y - 1][pos_x - 1] = num
                formatted_print(message, sudoku_unsolved)

            if sudoku_unsolved == sudoku_solved and f0:
                f0 = False
                bot.send_message(message.from_user.id, "Поздравляю, вы прошли уровень")
        except ValueError:
            bot.send_message(message.from_user.id, 'Вы должны вводить данные по правилам!')

    print(sudoku_solved)


last_char = '1'
flag_0 = True
mistakes = 0
f0 = True
cities_branch = False
sudoku_branch = False

# Запускаем работу бота
bot.polling(none_stop=True, interval=0)
