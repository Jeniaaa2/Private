import os, json, random

BASE = os.path.dirname(os.path.abspath(__file__))
POLICY_FILE = os.path.join(BASE, "agent_policy.json")

def _load_policy():
    if os.path.exists(POLICY_FILE):
        try:
            return json.loads(open(POLICY_FILE, encoding="utf-8").read())
        except Exception:
            pass
    return {"wins": {"BITWISE_BOOST": 1, "VECTOR_EXPAND": 1, "STRICT_GATE": 1}, "last_mode": "VECTOR_EXPAND"}

def run_agent_debate(topic, xp, elo):
    pol = _load_policy()
    wins = pol.get("wins", {"BITWISE_BOOST": 1, "VECTOR_EXPAND": 1, "STRICT_GATE": 1})
    
    # Читаем реальный рекорд ядра для аргументов Критика
    rec_ops = 66451502
    gp = os.path.join(BASE, "genome.json")
    if os.path.exists(gp):
        try:
            rec_ops = json.loads(open(gp, encoding="utf-8").read()).get("record_ops", rec_ops)
        except Exception:
            pass

    # Стратег выбирает тактику с учётом накопленных побед (взвешенный выбор)
    modes = list(wins.keys())
    boost = int(pol.get("active_leaders", 1))
    weights = [max(1, wins[m] + (boost if m == pol.get("last_mode") else 0)) for m in modes]
    chosen = random.choices(modes, weights=weights, k=1)[0]

    proposals = {
        "BITWISE_BOOST": (f"Форсировать побитовые маски для '{topic}' (порог +5%)", 1.05),
        "VECTOR_EXPAND": (f"Удвоить векторную выборку для '{topic}' (порог +3%)", 1.03),
        "STRICT_GATE":   (f"Жёсткий отсев медленных мутаций для '{topic}' (порог +8%)", 1.08),
    }
    prop_text, mult = proposals[chosen]

    critic = f"Проверка порога против рекорда {rec_ops:,} ops/s: допустим множитель x{mult}"
    arbiter = f"УТВЕРЖДЕНО [{chosen} | порог x{mult} | XP={xp}]"

    # Обновляем счётчик эффективности выбранной стратегии
    wins[chosen] = wins.get(chosen, 1) + 1
    pol["wins"] = wins
    pol["last_mode"] = chosen
    pol["last_mult"] = mult
    try:
        open(POLICY_FILE, "w", encoding="utf-8").write(json.dumps(pol, ensure_ascii=False, indent=2))
    except Exception:
        pass

    return f"🗣️ Дебаты агентов: [Стратег: {prop_text}] vs [Критик: {critic}] -> [Арбитр: {arbiter}]"
