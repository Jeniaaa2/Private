import math, random, hashlib
# Автономный серверный модуль по теме: Distributed Consensus
random.seed(18)
weights = [round(random.uniform(0.1, 1.0), 4) for _ in range(6)]
entropy = -sum((w/sum(weights)) * math.log2(w/sum(weights)) for w in weights)
sig = hashlib.sha256("Distributed Consensus".encode()).hexdigest()[:12]
print(f"Тема: Distributed Consensus | Энтропия весов: {entropy:.4f} | Сигнатура: {sig}")
