# Evolved Gen #42 (Attempt #1): Битбордовая генерация ходов
import math, cmath, time
freq_in = (27813 % 15) + 1
t0 = time.perf_counter()
N = 16
signal = {k: complex(math.cos(2 * math.pi * freq_in * k / N), 0.0) for k in range(N)}
qft = {m: sum(signal.get(k, 0j) * cmath.exp(-2j * math.pi * k * m / N) for k in range(N)) / math.sqrt(N) for m in range(N)}
probs = {m: round(abs(amp) ** 2, 4) for m, amp in qft.items()}
peak_m = max(probs, key=lambda k: probs.get(k, 0.0))
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'Квантовый QFT [Битбордовая генерация ходов]: гармоника={peak_m}, пик_P={round(probs.get(peak_m, 0)*100, 1)}%, время={dt} мкс')
