# Evolved Gen #10 (Attempt #2): Графовые эвристики в шахматных движках
import math, zlib, time
topic = 'Графовые эвристики в шахматных движках'
intel = '[Wiki EN] Stockfish (chess): Stockfish is a free and open-source chess engine, available for various desktop and mobile platforms. It can be used in chess software through the Universal Chess Interface'
t0 = time.perf_counter()
raw = (topic + ' | ' + intel).encode('utf-8') * 12
comp = zlib.compress(raw, level=9)
ratio = round((1 - len(comp) / max(1, len(raw))) * 100, 2)
entropy = round(-sum((raw.count(b)/len(raw))*math.log2(raw.count(b)/len(raw)) for b in set(raw)), 4)
dt_ms = round((time.perf_counter() - t0) * 1000, 3)
print(f'Алгоритм [{topic}]: сжатие={ratio}%, энтропия={entropy} бит, время={dt_ms} мс')
