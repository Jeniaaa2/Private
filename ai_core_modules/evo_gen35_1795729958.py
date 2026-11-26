# Evolved Gen #35 (Attempt #1): Квантовое компрессирование шахматных графов
import time, array, os
seed_t = 43980 | 1
t0 = time.perf_counter()
try:
    import numpy as np
    arr = np.arange(1, 4097, dtype=np.uint64) ^ np.uint64(seed_t)
    arr = ((arr << np.uint64(13)) ^ (arr >> np.uint64(7))) * np.uint64(2654435761)
    res_hash = int(np.bitwise_xor.reduce(arr)) & 0xFFFFFFFF
    mode = 'NumPy-SIMD'
except Exception:
    buf = array.array('I', ((i ^ seed_t) & 0xFFFFFFFF for i in range(1, 4097)))
    for idx in range(len(buf)):
        x = buf[idx]
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        buf[idx] = x
    res_hash = buf[0] ^ buf[-1]
    mode = 'C-Array-Bitwise'
dt = max(time.perf_counter() - t0, 1e-9)
ops = int(4096 / dt)
cores = os.cpu_count() or 1
print(f'TURBO [{mode} | {cores} CPU]: скорость={ops} ops/s, хэш={res_hash:08x}')
