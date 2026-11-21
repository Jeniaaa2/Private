import hashlib, os, textwrap

def one_way_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

# Sample plaintext
plaintext = textwrap.dedent("""
    Это пример текста, который будет зашифрован.
    Используем одинарный шифр SHA-256.
""").strip()

# Generate a random salt and combine it with the plaintext for better security
salt = os.urandom(16).hex()
combined = salt + plaintext

# Compute the hash
hashed_value = one_way_hash(combined)

print(f"Соль: {salt}")
print(f"Хеш SHA-256: {hashed_value}")