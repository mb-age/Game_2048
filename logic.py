import copy
import random
from itertools import chain
from typing import List


def get_number_from_index(i, j):
    return i * 4 + j + 1


def get_index_from_number(num):
    num -= 1
    x, y = num // 4, num % 4
    return x, y


def insert_2_or_4(mas, x, y):
    if random.random() < 0.75:
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas


def get_empty_list(mas):
    empty = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                num = get_number_from_index(i, j)
                empty.append(num)
    return empty


def is_zero_in_mas(mas):
    for row in mas:
        if 0 in row:
            return True
    return False


def move_left(mas: List[list]):
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


def move_right(mas: List[list]):
    mas_buf = copy.deepcopy(mas)
    mas, delta, biggest_number, _ = move_left(mas)
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    return mas, delta, biggest_number, mas != mas_buf


def move_down(mas: List[list]):
    mas_buf = copy.deepcopy(mas)
    mas = list(zip(*mas[::-1]))
    mas, delta, biggest_number, _ = move_left(mas)
    mas = list(reversed(list(zip(*mas))))
    mas = [*map(list, mas)]
    return mas, delta, biggest_number, mas != mas_buf


def move_up(mas: List[list]):
    mas_buf = copy.deepcopy(mas)
    mas = list(reversed(list(zip(*mas))))
    mas, delta, biggest_number, _ = move_left(mas)
    mas = list(zip(*mas[::-1]))
    mas = [*map(list, mas)]
    return mas, delta, biggest_number, mas != mas_buf


def can_move(mas):
    for i in range(3):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] or mas[i][j] == mas[i + 1][j]:
                return True
    for i in range(1, 4):
        for j in range(1, 4):
            if mas[i][j] == mas[i][j - 1] or mas[i][j] == mas[i - 1][j]:
                return True
    return False
