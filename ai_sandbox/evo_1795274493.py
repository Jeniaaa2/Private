from collections import defaultdict, deque

# Строим простой граф как словарь смежности
graph = defaultdict(list)
edges = [
    (1, 2), (1, 3), (2, 3),
    (2, 4), (3, 5), (4, 5),
    (5, 6)
]
for a, b in edges:
    graph[a].append(b)
    graph[b].append(a)

# Функция для поиска кратчайшего пути по BFS
def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

# Пример использования: найти путь от вершины 1 до 6
path = bfs(1, 6)

print("Кратчайший путь от 1 до 6:", path)