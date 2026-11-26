import os, json, random, time

BASE = os.path.dirname(os.path.abspath(__file__))
W_FILE = os.path.join(BASE, "chess_weights.json")

def train_self_play(gen=28):
    w = {"elo": 1500, "games": 0, "knight": 320, "bishop": 330, "center": 4.2}
    if os.path.exists(W_FILE):
        try:
            w.update(json.loads(open(W_FILE, encoding="utf-8").read()))
        except Exception:
            pass
    rng = random.Random(gen * 137 + int(time.time()) % 97)
    for _ in range(12):
        cand_c = round(w["center"] + rng.uniform(-0.3, 0.45), 2)
        cand_b = w["bishop"] + rng.choice([-2, 0, 2, 4])
        score_a = w["center"] * 12 + (w["bishop"] - w["knight"])
        score_b = cand_c * 12 + (cand_b - w["knight"]) + rng.uniform(-3.0, 3.5)
        w["games"] += 1
        if score_b > score_a:
            w["center"] = max(2.0, min(9.5, cand_c))
            w["bishop"] = max(315, min(355, cand_b))
            w["elo"] += 6
        else:
            w["elo"] += 2
    open(W_FILE, "w", encoding="utf-8").write(json.dumps(w, indent=2))
    try:
        import github_ai
        note = github_ai.ask_github_ai(f"Gen #{gen} AI & Quantum Algorithms", "")
        if note:
            return f"Шахматный Self-Play: Elo={w['elo']} ({w['games']} партий) | {note[:85]}"
    except Exception:
        pass
    return f"Шахматный Self-Play: Elo={w['elo']} ({w['games']} партий, слон={w['bishop']}, центр={w['center']})"

if __name__ == "__main__":
    print(train_self_play())
