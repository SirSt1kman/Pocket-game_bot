import pandas as pd

# получаем ссылку на страницу
URL = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8'
# создаём таблицу из данных на сайте
table = pd.read_html(URL)[0]
# получаем колонку таблицы с названиями городов
cities_column = table['Город']
# создаём обычный список из найденных городов
cities_list = [city for city in cities_column]
