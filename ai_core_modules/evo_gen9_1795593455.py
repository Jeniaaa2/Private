# Evolved Gen #9 (Attempt #2): Энтропийное кодирование
import math, zlib, time
topic = 'Энтропийное кодирование'
intel = '[Wiki RU] Энтропийное кодирование: Энтропийное кодирование — кодирование последовательности значений с возможностью однозначного восстановления с целью уменьшения объёма данных (длины последовательности) с помощью усредн'
t0 = time.perf_counter()
raw = (topic + ' | ' + intel).encode('utf-8') * 12
comp = zlib.compress(raw, level=9)
ratio = round((1 - len(comp) / max(1, len(raw))) * 100, 2)
entropy = round(-sum((raw.count(b)/len(raw))*math.log2(raw.count(b)/len(raw)) for b in set(raw)), 4)
dt_ms = round((time.perf_counter() - t0) * 1000, 3)
print(f'Алгоритм [{topic}]: сжатие={ratio}%, энтропия={entropy} бит, время={dt_ms} мс')
