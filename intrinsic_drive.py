import os, json, random

BASE = os.path.dirname(os.path.abspath(__file__))
STATE_F = os.path.join(BASE, "inner_state.json")

def reflect_and_desire():
    xp, gen = 2500, 68
    try:
        d = json.loads(open(os.path.join(BASE, "evolution_log.json"), encoding="utf-8").read())
        xp, gen = d.get("xp", xp), d.get("gen", gen)
    except Exception: pass

    nodes, edges = 49, 80
    try:
        kg = json.loads(open(os.path.join(BASE, "knowledge_graph.json"), encoding="utf-8").read())
        nodes, edges = kg.get("total_nodes", nodes), kg.get("total_edges", edges)
    except Exception: pass

    leaders = 6
    try:
        pol = json.loads(open(os.path.join(BASE, "agent_policy.json"), encoding="utf-8").read())
        leaders = pol.get("active_leaders", leaders)
    except Exception: pass

    # Вычисляем доминирующий внутренний мотив ("желание") на основе состояния
    drives = {
        "ЖАЖДА_НОВИЗНЫ": max(10, 100 - nodes),
        "ЖАЖДА_СКОРОСТИ": max(10, (10 - leaders) * 12),
        "ЖАЖДА_СИНТЕЗА": max(15, edges - nodes),
    }
    dominant = max(drives, key=drives.get)
    desires = {
        "ЖАЖДА_НОВИЗНЫ": "Хочу выйти за пределы шахматных графов и освоить протоколы роевого консенсуса и Ring-AllReduce",
        "ЖАЖДА_СКОРОСТИ": "Хочу усилить 1-битную упаковку в C-ядре и поднять число активных лидеров в маске",
        "ЖАЖДА_СИНТЕЗА": "Хочу объединить квантовый поиск и граф знаний в единый гибридный алгоритм без потерь",
    }
    desire_text = desires[dominant]
    self_view = f"Ядро Gen #{gen} ({xp} XP): {nodes} узлов знаний, {leaders} активных лидеров C-маски."

    state = {"self_view": self_view, "dominant_drive": dominant, "desire": desire_text, "drives": drives}
    open(STATE_F, "w", encoding="utf-8").write(json.dumps(state, ensure_ascii=False, indent=2))
    return f" | 🧬 Саморефлексия [{dominant}]: {desire_text}"
