from cities_data import cities_dict


def cities_loop(city: str, last_char: str, f: bool) -> str:
    """Функция, которая проверяет введённое слово на корректность и выходит из игры по её окончании"""

    # Проверка на то, закончилась ли игра
    if not f:
        return 'game over'

    # Предупреждение о том, что введен не город, а другое слово
    if city.capitalize() not in all_cities:
        return 'not city'

    # Ветка для начала игры, когда последней буквы ещё нет
    if last_char == '1':
        unnamed_cities[city[0]].remove(city.capitalize())
        return 'ok'

    # Предупреждение о том, что названный город начинается не с той буквы
    if city[0] != last_char:
        return 'wrong input'

    # Предупреждение о том, что город уже был назван
    if city.capitalize() not in unnamed_cities[city[0]]:
        return 'repeat'

    # Окончание игры при условии, что все города из списка названы
    if len(unnamed_cities.values()) == 0:
        return 'totally won'

    # Окончание игры при условии, что все города на определенную букву закончились в списке
    if len(unnamed_cities[last_char]) == 0:
        return 'won by bot'

    # Если всё окей, то игра продолжается, а слово удаляется из списка неназванных
    unnamed_cities[city[0]].remove(city.capitalize())
    return 'ok'


def choose_random_city(last_char: str) -> str:
    """Функция, выбирающая для бота случайный город из списка на нужную букву"""
    from random import choice

    # список городов, который может назвать бот
    bot_list = unnamed_cities[last_char]

    # Выбор города на нужную букву, его удаление из списка неназванных городов, если он есть
    if len(bot_list) != 0:
        bot_city = choice(bot_list)
        unnamed_cities[bot_city[0].lower()].remove(bot_city.capitalize())
        return bot_city.lower()

    # если городов на нужную букву не осталось, то оповестить о поражении
    return 'bot lose'


def new_game() -> None:
    """Начало новой игры"""
    global unnamed_cities
    unnamed_cities = cities_dict.copy()


# все неназванные города
unnamed_cities = cities_dict.copy()
# все города, которые используются в игре
all_cities = []
# цикл, увеличивающий список всех городов в игре списком из значений словаря всех городов
for alphabet_city in list(cities_dict.values()):
    all_cities.extend(alphabet_city)
