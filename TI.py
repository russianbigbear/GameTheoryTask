# -*- coding: utf8 -*-
import numpy as np
from scipy.optimize import linprog


def read_data(file_name):
    """Считывание данных и файла"""
    print('Чтение платежной матрицы из файла ' + file_name)

    # считывание матрицы в список А
    try:
        _matrix = open(file_name).read()
        _a = [list(map(float, item.split())) for item in _matrix.split('\n')[:-1]]
    except:
        print("Файла не существует или введеные данные некоректны!")
        raise SystemExit()

    # в каждой строке должно быть одинаковое количество элементов
    _n = len(_a)  # число строк матрицы А
    _m = len(_a[0])  # число столбцов матрицы А
    is_ok = 1
    for i in range(2, _n):
        if len(_a[i]) != _m:
            is_ok = 0

    if is_ok == 0:
        print("Строки разной длины!")
        raise SystemExit()

    return np.array(_a)


def print_list(_matrix):
    """Вывод платежной матрицы"""

    print("Платежная матрица: ")
    for i in range(len(_matrix)):
        print(_matrix[i])
    print("")


def solve_game(_a, pflag=0):
    """Решение задачи ТИ, сведением к ЛП"""

    # определение оптимальной стратегии 2 игрока

    d_c = np.amin(_a)  # минимальный элемент в матрице
    if d_c < 0:
        # добавление константы к элементам матрицы, чтобы они были положительными
        _a = _a - d_c
    else:
        d_c = 0

    # параметры задачи линейного программирования для 1 игрока
    c = np.ones(len(_a))  # целевая функция
    a_ub = -np.transpose(_a)  # коэффициенты ограничений
    b_ub = -np.ones(len(_a[0]))  # правые части ограничений
    result_a = linprog(c, a_ub, b_ub)  # находит min f'*x, если A*x ,= b

    # решение задачи ЛП для первого игрока
    if pflag:
        print(result_a)

    # оптимальная стратегия первого игрока   
    price = 1 / result_a.fun
    p_optimal = price * result_a.x

    # параметры задачи линейного программирования для 2 игрока
    c = -np.ones(len(_a[0]))  # целевая функция
    a_ub = _a  # коэффициенты ограничений
    b_ub = np.ones(len(_a))  # правые части ограничений
    result_b = linprog(c, a_ub, b_ub)

    # решение задачи ЛП для второго игрока
    if pflag:
        print(result_b)

    # оптимальная стратегия второго игрока   
    price = -1 / result_b.fun
    q_optimal = price * result_b.x

    return [price + d_c, p_optimal, q_optimal]


def main():
    # ввод файла
    file_name = input("Введите номер примера: ")
    a = read_data("Matrix" + file_name + ".dat")
    print_list(a)

    [c, p_opt, q_opt] = solve_game(a, 0)
    print("РЕШЕНИЕ ЗАДАЧИ ИГРЫ:")
    print("Цена игры: " + str(c) + "\n")
    print('Оптимальная стратегия первого игрока: ', end=' ')
    print(p_opt)
    print('Оптимальная стратегия второго игрока: ', end=' ')
    print(q_opt)


if __name__ == '__main__':
    main()
