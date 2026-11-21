import hashlib
import json
import time
from pathlib import Path

def generate_electronic_trail(events):
    """Создаёт простую цепочку событий, хешируя предыдущий чек и текущий."""
    trail = []
    prev_hash = '0' * 64  # начальный «корневой» хеш
    for i, event in enumerate(events, 1):
        data = json.dumps(event, sort_keys=True)
        combined = prev_hash + data + str(time.time())
        curr_hash = hashlib.sha256(combined.encode()).hexdigest()
        trail.append({
            'event': event,
            'hash': curr_hash,
            'prev_hash': prev_hash,
            'time': time.time(),
        })
        prev_hash = curr_hash
    return trail

def main():
    sample_events = [
        {'action': 'login', 'user': 'alice', 'ip': '192.168.0.5'},
        {'action': 'upload', 'user': 'alice', 'file': 'report.pdf'},
        {'action': 'logout', 'user': 'alice'},
    ]
    trail = generate_electronic_trail(sample_events)
    output_file = Path('electronic_trail.json')
    output_file.write_text(json.dumps(trail, indent=2))
    print(f'Электронный след записан в {output_file.resolve()}')

if __name__ == '__main__':
    main()