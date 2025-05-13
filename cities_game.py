from test_data import cities_list


def cities_loop(city: str, last_char: str, f: bool) -> str:
    """Функция, которая проверяет введённое слово на корректность и выходит из игры по её окончании"""

    # Проверка на то, закончилась ли игра
    if not f:
        return 'game over'

    # Предупреждение о том, что введен не город, а другое слово
    if city not in cities_list:
        return 'not city'

    # Предупреждение о том, что город уже был назван
    if city not in unnamed_cities:
        return 'repeat'

    # Ветка для начала игры, когда последней буквы ещё нет
    if last_char == '1':
        unnamed_cities.remove(city)
        return 'ok'

    # Предупреждение о том, что названный город начинается не с той буквы
    if city[0] != last_char:
        return 'wrong input'

    # Окончание игры при условии, что все города из списка названы
    if len(unnamed_cities) == 0:
        return 'totally won'

    # Окончание игры при условии, что все города на определенную букву закончились в списке
    if len([city_ for city_ in unnamed_cities if city_[0] == last_char]) == 0:
        return 'won by bot'

    # Если всё окей, то игра продолжается, а слово удаляется из списка неназванных
    unnamed_cities.remove(city)
    return 'ok'


def choose_random_city(last_char: str) -> str:
    """Функция, выбирающая для бота случайный город из списка на нужную букву"""
    from random import choice

    # список городов, который может назвать бот
    bot_list = [city_ for city_ in unnamed_cities if city_[0] == last_char]

    # Выбор города на нужную букву, его удаление из списка неназванных городов, если он есть
    if len(bot_list) != 0:
        bot_city = choice(bot_list)
        unnamed_cities.remove(bot_city)
        return bot_city

    # если городов на нужную букву не осталось, то оповестить о поражении
    return 'bot lose'


def new_game() -> None:
    """Начало новой игры"""
    global unnamed_cities
    unnamed_cities = cities_list[:]


unnamed_cities = cities_list[:]
