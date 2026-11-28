# Evolved Gen #77 (Attempt #1): Поиск по графу Монте-Карло
import time, random, os
seed_np = 25202
t0 = time.perf_counter()
rng = random.Random(seed_np)
n_vars, n_clauses = 12, 48
clauses = [tuple((rng.randint(1, n_vars), rng.choice((-1, 1))) for _ in range(3)) for _ in range(n_clauses)]
# Полиномиальная верификация случайного сертификата за O(n) (класс NP)
assign = {v: rng.choice((True, False)) for v in range(1, n_vars + 1)}
sat = sum(1 for cl in clauses if any((assign.get(v, False) if sgn == 1 else not assign.get(v, False)) for v, sgn in cl))
ratio = round((sat / n_clauses) * 100.0, 1)
dt = round((time.perf_counter() - t0) * 1e6, 2)
gy = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graveyard.md')
if ratio < 92.0 and os.path.isdir(os.path.dirname(gy)):
    with open(gy, 'a', encoding='utf-8') as f:
        f.write(f'- [Тупик 3-SAT | Поиск по графу Монте-Карло] Покрытие={ratio}% < 92% — жадная эвристика отброшена\n')
print(f'P vs NP 3-SAT [Поиск по графу Монте-Карло]: выполнено={sat}/{n_clauses} ({ratio}%), проверка_NP={dt} мкс')
