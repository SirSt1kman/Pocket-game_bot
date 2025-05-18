from sudoku_generator import Table, sudoku_unsolved, sudoku_solved
import sudoku_solver


def sudoku_loop(x_pos: int, y_pos: int, num: int, mistakes: int, f0: bool) -> str:
    """Функция, проверяющая верность хода при поставленной цифре num
    на выбранную клетку с позицией x_pos, y_pos"""

    # Проверка, закончилась ли игра
    if not f0:
        return 'already played'

    # Проверка, закончились ли жизни у пользователя
    if mistakes == 3:
        return 'lose'

    # Проверка вхождения координат в их диапазоне значений
    if x_pos < 1 or y_pos < 1 or x_pos > 9 or y_pos > 9:
        return 'wrong position'

    # Проверка вхождения выбранного числа в его диапазоне значений
    if num < 1 or num > 9:
        return 'wrong number'

    # Проверка на то, стоит ли на выбранной позиции цифра
    if sudoku_unsolved[y_pos - 1][x_pos - 1] != 0:
        return 'already num'

    # Предупреждение о неправильно выбранной цифре
    if num != sudoku_solved[y_pos - 1][x_pos - 1]:
        return 'mistake'

    # Случай, при котором поставленная цифра правильная
    return 'ok'


def new_game_sudoku():
    """Рестарт игры в судоку"""

    sudoku1 = Table()
    sudoku_copy1 = Table()
    sudoku1.mixed_swapping(100)
    sudoku1.delete_elements(30)
    sudoku_unsolved = sudoku1.return_array_grid()
    sudoku_copy1.table = [line[:] for line in sudoku_unsolved]
    sudoku_solved = list(sudoku_solver.solve_sudoku(sudoku_copy1.return_array_grid()))[0]

    return sudoku_unsolved, sudoku_solved