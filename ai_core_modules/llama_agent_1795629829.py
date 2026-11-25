# Агент-резерв (Llama оффлайн) | Тема: эвристическая оценка шахматной позиции по битовым маскам
import math, time
t0 = time.perf_counter()
vals = [math.sin(i * 0.37) ** 2 for i in range(64)]
norm = round(sum(vals), 4)
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'Резервный агент [эвристическая оценка шахматной позиции по битовым маскам]: сумма_амплитуд={norm}, время={dt} мкс')
