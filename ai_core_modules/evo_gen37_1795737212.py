# Evolved Gen #37 (Attempt #1): Шахматные графовые S-box
import time, random
random.seed(19549)
table = {(p_id, sq): random.getrandbits(64) for p_id in range(12) for sq in range(64)}
t0 = time.perf_counter()
h = 0
for p_id in range(12): h ^= table.get((p_id, (p_id * 5 + 3) % 64), 0)
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'Zobrist Hash [Шахматные графовые S-box]: ключ={hex(h)[:14]}, время={dt} мкс')
