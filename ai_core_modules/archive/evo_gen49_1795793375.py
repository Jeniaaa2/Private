# Evolved Gen #49 (Attempt #1): Графовое сжатие шахматных позиций
import time, random
random.seed(33404)
table = {(p_id, sq): random.getrandbits(64) for p_id in range(12) for sq in range(64)}
t0 = time.perf_counter()
h = 0
for p_id in range(12): h ^= table.get((p_id, (p_id * 5 + 3) % 64), 0)
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'Zobrist Hash [Графовое сжатие шахматных позиций]: ключ={hex(h)[:14]}, время={dt} мкс')
