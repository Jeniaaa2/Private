# Evolved Gen #20 (Attempt #1): Обучение с подкреплением
import math, time, random
random.seed(24194)
sig = lambda x: 1 / (1 + math.exp(-max(-20, min(20, x))))
t0 = time.perf_counter()
w11, w12, w21, w22, v1, v2 = (random.uniform(-1, 1) for _ in range(6))
for _ in range(400):
    for x1, x2, y in ((0,0,0),(0,1,1),(1,0,1),(1,1,0)):
        h1, h2 = sig(x1*w11 + x2*w12), sig(x1*w21 + x2*w22)
        out = sig(h1*v1 + h2*v2); err = y - out
        v1 += 0.5*err*h1; v2 += 0.5*err*h2
dt = round((time.perf_counter() - t0) * 1000, 3)
print(f'Нейросеть XOR [Обучение с подкреплением]: финальная_ошибка={round(abs(err), 4)}, эпох=400, время={dt} мс')
