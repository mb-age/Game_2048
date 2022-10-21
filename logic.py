""" Logics of the game """

import copy
import random
from itertools import chain
from typing import List, Tuple


def get_number_from_index(i: int, j: int) -> int:
    """ Takes number of row and column and gets ordinal number of the cell """
    return i * 4 + j + 1


def get_index_from_number(num: int) -> Tuple[int]:
    """ Takes ordinal number of the cell and gets number of row and column """
    num -= 1
    x, y = num // 4, num % 4
    return x, y


def insert_2_or_4(mas: List[list], x: int, y: int) -> List[list]:
    """ Inserts 2 or 4 to the random free place of the playing field """
    if random.random() < 0.75:
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas


def get_empty_list(mas: List[list]) -> List[int]:
    """ Gets a list of ordinal numbers of all the free cels """
    empty = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                num = get_number_from_index(i, j)
                empty.append(num)
    return empty


def is_zero_in_mas(mas: List[list]) -> bool:
    """ Checks if there free cells on the play field """
    for row in mas:
        if 0 in row:
            return True
    return False


def move_left(mas: List[list]) -> tuple:
    """ Moves all numbers to the left, gets a sum of two same numbers """
    mas = [*map(list, mas)]
    mas_buf = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j + 1)
                mas[i].append(0)
    biggest_number = max(chain(*mas))
    return mas, delta, biggest_number, mas != mas_buf


def move_right(mas: List[list]) -> tuple:
    """ Moves all numbers to the right, gets a sum of two same numbers """
    mas_buf = copy.deepcopy(mas)
    mas, delta, biggest_number, _ = move_left(mas)
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    return mas, delta, biggest_number, mas != mas_buf


def move_down(mas: List[list]) -> tuple:
    """ Moves all numbers down, gets a sum of two same numbers """
    mas_buf = copy.deepcopy(mas)
    mas = list(zip(*mas[::-1]))
    mas, delta, biggest_number, _ = move_left(mas)
    mas = list(reversed(list(zip(*mas))))
    mas = [*map(list, mas)]
    return mas, delta, biggest_number, mas != mas_buf


def move_up(mas: List[list]) -> tuple:
    """ Moves all numbers up, gets a sum of two same numbers """
    mas_buf = copy.deepcopy(mas)
    mas = list(reversed(list(zip(*mas))))
    mas, delta, biggest_number, _ = move_left(mas)
    mas = list(zip(*mas[::-1]))
    mas = [*map(list, mas)]
    return mas, delta, biggest_number, mas != mas_buf


def can_move(mas: List[list]) -> bool:
    """ Cheks if there can be sum of two same numbers """
    for i in range(3):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] or mas[i][j] == mas[i + 1][j]:
                return True
    for i in range(1, 4):
        for j in range(1, 4):
            if mas[i][j] == mas[i][j - 1] or mas[i][j] == mas[i - 1][j]:
                return True
    return False
