# Evolved Gen #56 (Attempt #1): Эндшпильные базы сжатия
import heapq, time
from collections import Counter
sample = ('Эндшпильные базы сжатия' + ' ' + '[Wiki EN] Endgame tablebase: In chess, an endgame tablebase, or simply tablebase, is a computerised database containing precalculated evaluations of endgame positions. Tablebases a') * 5
t0 = time.perf_counter()
freq = Counter(sample)
heap = [(w, id(ch), {ch: ''}) for ch, w in freq.items()]
heapq.heapify(heap)
while len(heap) > 1:
    w1, _, d1 = heapq.heappop(heap)
    w2, _, d2 = heapq.heappop(heap)
    merged = {k: '0' + v for k, v in d1.items()}
    merged.update({k: '1' + v for k, v in d2.items()})
    heapq.heappush(heap, (w1 + w2, id(merged), merged))
_, _, codes = heap.pop() if heap else (0, 0, {})
bits = sum(len(codes.get(c, '0')) for c in sample)
dt = round((time.perf_counter() - t0) * 1000, 3)
print(f'Хаффман-кодер [Эндшпильные базы сжатия]: было={len(sample)*8} бит -> стало={bits} бит, время={dt} мс')
