# Evolved Gen #28 (Attempt #1): Квантовый граф‑алгоритм
import heapq, time
t0 = time.perf_counter()
grid = {(x, y): (x + y) % 3 + 1 for x in range(8) for y in range(8)}
pq, cost = [(0, 0, 0)], {(0, 0): 0}
while pq:
    _, cx, cy = heapq.heappop(pq)
    if (cx, cy) == (7, 7): break
    for dx, dy in ((1,0),(0,1),(-1,0),(0,-1)):
        nx, ny = cx + dx, cy + dy
        if (nx, ny) in grid and cost.get((cx, cy)) + grid.get((nx, ny)) < cost.get((nx, ny), 9999):
            cost[(nx, ny)] = cost.get((cx, cy)) + grid.get((nx, ny))
            heapq.heappush(pq, (cost.get((nx, ny)) + abs(7 - nx) + abs(7 - ny), nx, ny))
dt = round((time.perf_counter() - t0) * 1000, 3)
print(f'A* Граф 8x8 [Квантовый граф‑алгоритм]: цена_пути={cost.get((7, 7))}, узлов={len(cost)}, время={dt} мс')
