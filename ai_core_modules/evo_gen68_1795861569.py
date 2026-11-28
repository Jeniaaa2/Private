# Evolved Gen #68 (Attempt #1): Поиск Монте-Карло по дереву
import math, cmath, time
steps = 10 + (26114 % 8)
t0 = time.perf_counter()
nodes = 12
amp = {i: complex(1.0 / math.sqrt(nodes), 0.0) for i in range(nodes)}
for st in range(steps):
    amp = {i: 0.5 * (amp.get((i - 1) % nodes, 0j) + 1j * amp.get((i + 1) % nodes, 0j)) for i in range(nodes)}
    norm = math.sqrt(sum(abs(v) ** 2 for v in amp.values())) or 1.0
    amp = {i: v / norm for i, v in amp.items()}
max_node = max(amp, key=lambda k: abs(amp.get(k, 0j)) ** 2)
max_p = round((abs(amp.get(max_node, 0j)) ** 2) * 100.0, 2)
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'Quantum Walk [Поиск Монте-Карло по дереву]: шагов={steps}, узел_пика={max_node}, P={max_p}%, время={dt} мкс')
