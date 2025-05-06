from itertools import product


def solve_sudoku(grid: list):
    """Функция, решающая судоку размером size и готовой частью сетки судоку grid"""
    x = ([("rc", rc) for rc in product(range(9), range(9))] +
         [("rn", rn) for rn in product(range(9), range(1, 10))] +
         [("cn", cn) for cn in product(range(9), range(1, 10))] +
         [("bn", bn) for bn in product(range(9), range(1, 10))])
    y = dict()

    for row, col, n in product(range(9), range(9), range(1, 10)):
        b = (row // 3) * 3 + (col // 3)  # Box number
        y[(row, col, n)] = [
            ("rc", (row, col)),
            ("rn", (row, n)),
            ("cn", (col, n)),
            ("bn", (b, n))]
    x, y = exact_cover(x, y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(x, y, (i, j, n))
    for solution in solve(x, y, []):
        for (row, col, n) in solution:
            grid[row][col] = n
        yield grid


def exact_cover(x, y):
    x = {j: set() for j in x}
    for i, row in y.items():
        for j in row:
            x[j].add(i)
    return x, y


def solve(x, y, solution):
    if not x:
        yield list(solution)
    else:
        c = min(x, key=lambda c: len(x[c]))
        for r in list(x[c]):
            solution.append(r)
            cols = select(x, y, r)
            for s in solve(x, y, solution):
                yield s
            deselect(x, y, r, cols)
            solution.pop()


def select(x, y, r):
    cols = []
    for j in y[r]:
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].remove(i)
        cols.append(x.pop(j))
    return cols


def deselect(x, y, r, cols):
    for j in reversed(y[r]):
        x[j] = cols.pop()
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].add(i)