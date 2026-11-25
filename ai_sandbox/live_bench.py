import time, zlib, hashlib, heapq
t0 = time.time()
t = 'Шахматные движки'
if "Сжатие" in t:
    raw = (b"AI_AGENT_DATA_STREAM_" * 200)
    comp = zlib.compress(raw)
    info = f"сжато {len(raw)} -> {len(comp)} байт ({round(100 - len(comp)*100/len(raw), 1)}% экономии)"
elif "Крипто" in t:
    h = hashlib.sha256(b"Gomel_Lab_2026").hexdigest()[:12]
    info = f"SHA-256 хеш-сигнатура={h}"
elif "графов" in t:
    g = {'A':[(2,'B'),(5,'C')],'B':[(1,'C'),(4,'D')],'C':[(1,'D')],'D':[]}
    pq, dist = [(0,'A')], {'A':0}
    while pq:
        d, u = heapq.heappop(pq)
        for w, v in g[u]:
            if d + w < dist.get(v, 999):
                dist[v] = d + w; heapq.heappush(pq, (dist[v], v))
    info = f"Дейкстра кратчайший путь A->D = {dist['D']}"
else:
    info = f"векторная оценка узлов = {sum(i*i for i in range(1, 51))}"
print(f"Песочница [{t}]: {info} ({round((time.time()-t0)*1000, 1)} мс)")
