import hashlib
import secrets
import math

# простая реализация протокола Шнорра (Schnorr ZKP)

# Набор параметров группы
# d = (p-1)/q должно быть целое число, где p и q простые
# Для простоты используем 2048‑битный p и 256‑битный q (не проверяем тут корректность :)
p = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED5290770969661"
    "17DA0D4D43D39AD02F6D7B01F5ECDC"
    "D1B8F1529DDAE9EC507C605B5E4C8C5"  # заглушка; фактическое p может быть другим
    , 16)
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD2  # заглушка

# Генератор группы
g = 2

# Функция хэша, используемая в протоколе
def H(*inputs):
    """Возвращает целое, мод q, из hash( ... )"""
    h = hashlib.sha256()
    for inp in inputs:
        if isinstance(inp, int):
            h.update(inp.to_bytes((inp.bit_length() + 7) // 8, 'big'))
        else:
            h.update(inp)
    return int.from_bytes(h.digest(), 'big') % q

# Утверждаемый секрет
x = secrets.randbelow(q)          # x ∈ [0, q-1]
# Соответствующий открытый ключ
y = pow(g, x, p)                   # y = g^x mod p

# ---------- Поставщик доказательства ----------
def generate_proof():
    """Создаёт одно доказательство без передачи x."""
    # 1. Случайный «промежуточный» выбор a ∈ [0, q-1]
    a = secrets.randbelow(q)
    # 2. Промежуточный открытый хэш r = g^a mod p
    r = pow(g, a, p)

    # 3. Задаём вызов c = H(g, y, r)
    c = H(g.to_bytes(256, 'big'),
          y.to_bytes(256, 'big'),
          r.to_bytes(256, 'big'))
    # 4. Вычисляем ответ: s = (a + c*x) mod q
    s = (a + c * x) % q

    # 5. Вернуть (y, r, s), где y - открытая часть ключа
    return y, r, s

# ---------- Проверка доказательства ----------
def verify_proof(y, r, s):
    """Проверяет доказательство, не зная x."""
    # 1. Пересчитываем вызов c
    c = H(g.to_bytes(256, 'big'),
          y.to_bytes(256, 'big'),
          r.to_bytes(256, 'big'))

    # 2. Проверяем уравнение: g^s ?= r * y^c  (mod p)
    lhs = pow(g, s, p)
    rhs = (r * pow(y, c, p)) % p
    return lhs == rhs

# ------ Тестируем --------
y_public, r_intermediate, s_answer = generate_proof()
result = verify_proof(y_public, r_intermediate, s_answer)

print("Zero‑Knowledge Proof verification result:", result)