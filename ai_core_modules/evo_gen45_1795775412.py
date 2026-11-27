# Evolved Gen #45 (Attempt #1): Блум-фильтр транспозиций
import math, time
phase = (24685 % 7) * 0.15
t0 = time.perf_counter()
# Состояние |Phi+> = (|00> + e^(i*phi)|11>) / sqrt(2)
a00 = complex(math.cos(phase) / math.sqrt(2), math.sin(phase) / math.sqrt(2))
a11 = complex(1.0 / math.sqrt(2), 0.0)
p00, p11 = round(abs(a00) ** 2, 4), round(abs(a11) ** 2, 4)
corr = round((p00 + p11) * 100.0, 2)
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'Запутанность Белла [Блум-фильтр транспозиций]: P(|00>)={p00}, P(|11>)={p11}, корреляция={corr}%, время={dt} мкс')
