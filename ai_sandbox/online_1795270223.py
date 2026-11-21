import math
import random
import itertools
import collections

# ------------------------------------------------------------------
# Нейрораспределённое связывание событий (простой имитационный пример)
# ------------------------------------------------------------------

# 1. Создадим простую «нейронную» сеть из узлов (нейронов)
NUM_NEURONS = 10
NEURON_IDS = range(NUM_NEURONS)

# 2. Каждому нейрону назначим случайный вес связи с другими нейронами
#    Веса – это числовые коэффициенты 0.0–1.0
weight_matrix = {
    (i, j): random.random()
    for i in NEURON_IDS
    for j in NEURON_IDS
    if i != j
}

# 3. Сгенерируем набор событий
#    Каждое событие имеет название и набор «активируемых» нейронов
NUM_EVENTS = 5
EVENTS = [
    {
        "name": f"event_{k}",
        "activators": random.sample(list(NEURON_IDS), k=random.randint(2, 5)),
    }
    for k in range(NUM_EVENTS)
]

# 4. Определим функцию «сущность связывания»:
#    При активации событий происходит динамическое распределение интенситета между нейронами
def bind_events(events, weight_map, neurons):
    """
    Возвращает словарь: нейрон -> суммарный «интенсив» после связывания.
    """
    # Вектор активности: сколько раз каждый нейрон активировался
    activation_counts = collections.Counter()

    for ev in events:
        # Считаем, что событие активирует все указанные нейроны
        activation_counts.update(ev["activators"])

    # Теперь считаем совокупный вклад веса каждого активированного нейрона
    result = {}
    for n in neurons:
        # Интенсивность = сумма весов от всех активировавших к нейрону n
        intensity = sum(
            weight_map.get((src, n), 0.0)
            for src in activation_counts
            if src != n
        )
        result[n] = intensity

    return result

# 5. Выполняем связывание
intensities = bind_events(EVENTS, weight_matrix, NEURON_IDS)

# 6. Выводим итог
print("Нейроны и их итоговый интенсив после связывания событий:")
for neuron_id, intensity in sorted(intensities.items()):
    # Округляем до 3 знаков после запятой для читаемости
    print(f"Нейрон {neuron_id:02d}: {intensity:.3f}")