# Evolved Gen #12 (Attempt #1): Шифрование графов
import heapq, time
topic = 'Шифрование графов'
g = {0: [(1, 4), (2, 2)], 1: [(3, 5)], 2: [(1, 1), (3, 8)], 3: [(4, 3)], 4: []}
t0 = time.perf_counter()
pq, dist = [(0, 0)], {0: 0}
while pq:
    d, u = heapq.heappop(pq)
    for v, w in g[u]:
        if d + w < dist.get(v, 999): dist[v] = d + w; heapq.heappush(pq, (dist[v], v))
dt = round((time.perf_counter() - t0) * 1000, 3)
print(f'Графовый оптимизатор [{topic}]: кратчайший путь={dist.get(4)}, время={dt} мс')
