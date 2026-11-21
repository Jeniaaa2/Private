import math
import random

# Квантовый объект, демонстрирующий «правила» для «доминированияпределы традиций»
class QuantumDominanceBoundary:
    def __init__(self, n=5):
        self.n = n
        # Инициализируем квантовую симуляцию случайными числами
        self.state = [random.random() for _ in range(n)]
        # Пределы традиций: всё, что находится в пределах ±0.5 относительно среднего
        self.tradition_threshold = 0.5

    def evolve(self):
        """Простейшая эволюция: смещение каждой компоненты на небольшое квантовое колебание."""
        self.state = [(x + random.gauss(0, 0.1)) % 1 for x in self.state]

    def measure(self):
        """Повернуть состояние так, чтобы оно либо стояло на границе, либо в пределах традиций."""
        avg = sum(self.state) / len(self.state)
        boundary = [0.0 if abs(x - avg) < self.tradition_threshold else 1.0 for x in self.state]
        return boundary

    def simulate(self, steps=10):
        """Запустить серию эволюции и измерений."""
        history = []
        for _ in range(steps):
            self.evolve()
            history.append(self.measure())
        return history

# Создание экземпляра и запуск симуляции
sim = QuantumDominanceBoundary()
history = sim.simulate(steps=15)

# Вывод результата
print("История измерений (0 - внутри традиций, 1 - за пределами):")
for i, step in enumerate(history, 1):
    print(f"Шаг {i}: {step}")