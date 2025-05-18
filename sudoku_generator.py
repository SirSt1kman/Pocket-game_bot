from random import randrange
from random import choice
import sudoku_solver

class Table:
    """Класс, описывающий таблицу, сетку судоку"""

    def __init__(self):
        """Генерация начальной сетки"""

        self.table = [[(j + 3 * i + i // 3) % 9 + 1 for j in range(9)] for i in range(9)]

        #  1 2 3    4 5 6    7 8 9
        #  4 5 6    7 8 9    1 2 3
        #  7 8 9    1 2 3    4 5 6
        #
        #  2 3 4    5 6 7    8 9 1
        #  5 6 7    8 9 1    2 3 4
        #  8 9 1    2 3 4    5 6 7
        #
        #  3 4 5    6 7 8    9 1 2
        #  6 7 8    9 1 2    3 4 5
        #  9 1 2    3 4 5    6 7 8

    def show(self):
        """Функция, выводящая сетку на экран"""

        for i in range(9):
            print(*self.table[i])

    def delete_elements(self, amount: int):
        """Функция, удаляющая случайные цифры из сетки судоку в количестве amount, пока в сетке
        будет оставаться единственное решение для данной раскладки судоку"""

        # счётчик клеток, цифры которых уже удалены
        i = 0
        # индексы ещё не отслеженных клеток с цифрами для данной раскладки
        marks = [(i, j) for i in range(9) for j in range(9)]

        # Продолжаем просматривать клетки и удалять некоторые из них, пока не превысим заданное количество клеток
        # или пока все клетки не будут просмотрены
        while i < amount and len(marks) > 0:
            # удаляем из непросмотренных меток просмотренную метку и оставляем элемент под этой меткой
            indexes = choice(marks)
            row_ind, col_ind = indexes[0], indexes[1]
            element = self.table[row_ind][col_ind]
            marks.remove((row_ind, col_ind))
            self.table[row_ind][col_ind] = 0

            # Проверяем данную раскладку на единственность решения
            solution_table = [self.table[j][:] for j in range(9)]
            solutions = 0

            # Добавляем решения с помощью решателя судоку
            for solution in sudoku_solver.solve_sudoku(solution_table):
                solutions += 1

            #Увеличиваем счётчик, если решение единственное, иначе возвращаем цифру в клетку и ищем другую
            if solutions == 1:
                i += 1
            else:
                self.table[row_ind][col_ind] = element

    def transposing(self) -> None:
        """Функция транспонирует сетку, перемешивая её"""

        self.table = list(map(list, zip(*self.table)))

    def swap_rows_mini(self) -> None:
        """Функция, меняющая местами два случайных ряда,
        находящихся в одной и той же тройке рядов"""

        # Случайный выбор тройки рядов
        sector = randrange(0, 3, 1)
        # Случайный выбор ряда, который не будет участвовать в перемешивании
        line1 = randrange(0, 3, 1)
        # Выбор оставшихся рядов для перемешивания
        lines = [i for i in range(3) if i != line1]
        row1, row2 = lines[0], lines[1]

        # меняем местами два ряда
        self.table[sector * 3 + row1], self.table[sector * 3 + row2] = \
            self.table[sector * 3 + row2], self.table[sector * 3 + row1]

    def swap_cols_mini(self) -> None:
        """Функция, меняющая местами два случайных столбца при помощи транспонирования"""

        self.transposing()
        self.swap_rows_mini()
        self.transposing()

    def swap_rows_maxi(self) -> None:
        """Функция, меняющая местами две случайных тройки рядов между собой"""

        # Случайный выбор тройки рядов, которую мы не будем перемешивать
        sector = randrange(0, 3, 1)
        # Выбор оставшихся троек для перемешивания
        sectors = [i for i in range(3) if i != sector]
        sector1, sector2 = sectors[0], sectors[1]

        # Цикл, меняющий местами каждый ряд одной тройки с каждым рядом другой тройки
        for j in range(3):
            self.table[sector1 * 3 + j], self.table[sector2 * 3 + j] = self.table[sector2 * 3 + j], self.table[sector1 * 3 + j]

    def swap_cols_maxi(self) -> None:
        """Функция, меняющая местами две случайных тройки столбцов между собой с помощью транспонирования"""

        self.transposing()
        self.swap_rows_maxi()
        self.transposing()

    def mixed_swapping(self, amount: int) -> None:
        """Функция, случайно перемешивающая поле с помощью известных функций в количестве раз amount"""

        # Список функций
        functions = ['self.transposing()', 'self.swap_rows_mini()', 'self.swap_cols_mini()',
                     'self.swap_rows_maxi()', 'self.swap_cols_maxi()']

        # Цикл, случайно использующий функции из списка functions в количестве amount
        for i in range(amount):
            eval(functions[randrange(0, len(functions), 1)])

    def return_array_grid(self) -> list:
        """Функция, возвращающая двумерный массив из клеток нерешенного судоку"""
        return self.table


sudoku = Table()
sudoku_copy = Table()
# sudoku.transposing()
# sudoku.swap_rows_mini()
# sudoku.swap_cols_mini()
# sudoku.swap_rows_maxi()
# sudoku.swap_cols_maxi()
sudoku.mixed_swapping(100)
sudoku.delete_elements(30)
# sudoku.show()

sudoku_unsolved = sudoku.return_array_grid()
sudoku_copy.table = [line[:] for line in sudoku_unsolved]
sudoku_solved = list(sudoku_solver.solve_sudoku(sudoku_copy.return_array_grid()))[0]

# print(sudoku_unsolved)
# print(sudoku_solved)
