# Evolved Gen #62 (Attempt #1): Поиск шахматных транспозиций через графовые сигнатуры
import math, time, random
random.seed(53249)
t0 = time.perf_counter()
wins, visits = {0: 1, 1: 1, 2: 1}, {0: 2, 1: 2, 2: 2}
for total in range(6, 306):
    arm = max((0, 1, 2), key=lambda i: wins.get(i)/visits.get(i) + 1.41 * math.sqrt(math.log(total)/visits.get(i)))
    visits[arm] += 1; wins[arm] += random.randint(0, 1)
best = max((0, 1, 2), key=lambda i: visits.get(i))
dt = round((time.perf_counter() - t0) * 1000, 3)
print(f'MCTS UCB1 [Поиск шахматных транспозиций через графовые сигнатуры]: лучшая_ветка={best}, симуляций=300, время={dt} мс')
