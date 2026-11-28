# Evolved Gen #59 (Attempt #1): Сжатие шахматных позиций
import math, cmath, time
target = 24892 % 32
t0 = time.perf_counter()
n_qubits = 5
dim = 1 << n_qubits
inv_s = 1.0 / math.sqrt(dim)
# Перевод регистра в равномерную квантовую суперпозицию H^5 |0>
state = {i: complex(inv_s, 0.0) for i in range(dim)}
# 4 итерации квантового оракула и диффузии Гровера (O(sqrt(N)))
for _ in range(4):
    state[target] = -state.get(target, 0j)
    mean_amp = sum(state.values()) / dim
    state = {i: 2.0 * mean_amp - amp for i, amp in state.items()}
probs = {i: abs(amp) ** 2 for i, amp in state.items()}
norm = round(sum(probs.values()), 6)
p_target = round(probs.get(target, 0.0) * 100.0, 2)
q_entropy = round(-sum(pr * math.log2(pr) for pr in probs.values() if pr > 1e-12), 4)
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'Квантовый поиск Гровера [Сжатие шахматных позиций]: |{target:05b}>, P={p_target}%, H_q={q_entropy} бит, Норма={norm}, время={dt} мкс')
