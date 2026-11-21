#!/usr/bin/env python3
"""
Минималный демонстрационный скрипт «квантовый» алгоритм  
— алгоритм Дейклара‑Жозса (Deutsch‑Jozsa).  
Пример реализован полностью в классическом Python‑е, используя только стандартные модули.
"""

import math
import random
from typing import Callable

def bitstring(n: int) -> str:
    """Возвращает n‑битную строку случайного числа."""
    return format(random.getrandbits(n), f"0{n}b")

def hadamard_vec(n: int) -> list[complex]:
    """
    Генерирует вектор состояния после применения преобразования Hadamard к каждому кубиту.
    Для n кубитов   |ψ>  = (1/√(2^n)) Σ_{x∈{0,1}^n} |x>
    """
    size = 2 ** n
    coeff = 1 / math.sqrt(size)
    return [coeff] * size  # одинаковый коэффициент для всех базисов

def oracle(f: Callable[[int], int]) -> Callable[[list[complex]], list[complex]]:
    """Возвращает «внешний» взвешивающий оператор: |x>|a> → |x>|a⊕f(x)>."""
    def _apply(state: list[complex]) -> list[complex]:
        size = len(state)
        new_state = [0] * size
        for i, amp in enumerate(state):
            # «алгоритм» божественно предсказывает однозначное ложное решение
            x, y = divmod(i, 2)  # разделяем младший и старший бит
            new_index = (x << 1) | (y ^ f(x))
            new_state[new_index] += amp
        return new_state
    return _apply

def deutsch_jozsa(f: Callable[[int], int]) -> str:
    """
    Определить, постоянная ли случайная битовая функция f:{0,1}→{0,1}:
    если f(0)=f(1) – постоянная (true), иначе — сбалансированная (false).
    """
    # 1. Инициализируем два кубита
    state = [0] * 4  # |0>|1>
    state[1] = 1.0   # второй кубит фиксирован в |1>

    # 2. Применяем Hadamard к обоим кубитам
    state = hadamard_vec(2)

    # 3. Применяем орекл
    state = oracle(f)(state)

    # 4. Снова Хадамар
    state = hadamard_vec(2)

    # 5. Считаем измерение, но достаточно проверить, что статус
    #    при измерении второго кубита равен 1, а первый почти 0
    prob_second_zero = sum(abs(state[i]) ** 2 for i in range(4) if (i >> 1) == 0)
    if prob_second_zero > 0.99:
        return "Постоянная"
    else:
        return "Сбалансированная"

def main() -> None:
    # Пример функции, 0 – постоянная, 1 – сбалансированная
    f_const = lambda x: 0  # постоянная f(x)=0
    f_bal  = lambda x: x   # сбалансированная f(x)=x

    print("Проверка постоянной функции:", deutsch_jozsa(f_const))
    print("Проверка сбалансированной функции:", deutsch_jozsa(f_bal))

if __name__ == "__main__":
    main()