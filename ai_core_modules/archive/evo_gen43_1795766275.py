# Evolved Gen #43 (Attempt #1): Сжатие нейросетевых оценок
import time, random, hashlib
seed_c = 26775
t0 = time.perf_counter()
rng = random.Random(seed_c)
q, n = 3329, 32
A = [[rng.randrange(q) for _ in range(n)] for _ in range(n)]
s_vec = [rng.choice((-1, 0, 1)) for _ in range(n)]
e_vec = [rng.choice((-1, 0, 1)) for _ in range(n)]
b_vec = [(sum(A[i][j] * s_vec[j] for j in range(n)) + e_vec[i]) % q for i in range(n)]
zk_proof = hashlib.sha3_256(str(b_vec[:8]).encode()).hexdigest()[:16]
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'PQC LWE-32 [Сжатие нейросетевых оценок]: модуль_q={q}, ZKP_хэш={zk_proof}, время={dt} мкс')
