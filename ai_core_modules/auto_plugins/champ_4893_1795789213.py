import re
from collections import Counter

_RX = re.compile(r'[^\w\s]')
_STOP = frozenset(('the', 'and', 'for', 'nor', 'but', 'a', 'an', 'of', 'in', 'on', 'to', 'from', 'by', 'with', 'that', 'this', 'is', 'are', 'как', 'для', 'или', 'при', 'что', 'это', 'без'))

def transform(text: str) -> str:
    words = [w for w in _RX.sub('', text.lower()).split() if len(w) > 3 and w not in _STOP]
    top_terms = [w for w, _ in Counter(words).most_common(8)]
    summary = ' '.join(text.split()[:40])
    return "Ключевые термины: " + ", ".join(top_terms) + ". Сводка: " + summary
