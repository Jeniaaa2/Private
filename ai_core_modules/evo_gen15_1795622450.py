# Evolved Gen #15 (Attempt #1): Графовое шифрование шахмат
import time, random
topic = 'Графовое шифрование шахмат'
def alphabeta(d, alpha, beta, max_p):
    if d == 0: return random.randint(-50, 50)
    v = -9999 if max_p else 9999
    for _ in range(3):
        val = alphabeta(d-1, alpha, beta, not max_p)
        if max_p: v = max(v, val); alpha = max(alpha, v)
        else: v = min(v, val); beta = min(beta, v)
        if beta <= alpha: break
    return v
t0 = time.perf_counter()
best = alphabeta(6, -9999, 9999, True)
dt = round((time.perf_counter() - t0) * 1000, 3)
print(f'Шахматный движок [{topic}]: оценка={best}, глубина=6, время={dt} мс')
