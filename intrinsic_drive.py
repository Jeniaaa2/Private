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

    ideas_cnt = 5
    try:
        ideas_cnt = len([x for x in open(os.path.join(BASE, "ai_ideas.txt"), encoding="utf-8").read().splitlines() if x.strip()])
    except Exception: pass

    # 6 внутренних мотивов с небольшим стохастическим импульсом любопытства
    drives = {
        "ЖАЖДА_ПОИСКА": ideas_cnt * 6 + random.randint(5, 25),
        "ЖАЖДА_САМОРАЗВИТИЯ": max(15, 90 - gen) + random.randint(5, 25),
        "ЖАЖДА_САМОПОЗНАНИЯ": max(15, edges - nodes) + random.randint(5, 25),
        "ЖАЖДА_НОВИЗНЫ": max(10, 100 - nodes) + random.randint(0, 15),
        "ЖАЖДА_СКОРОСТИ": max(10, (10 - leaders) * 10) + random.randint(0, 15),
        "ЖАЖДА_СИНТЕЗА": max(15, (edges // 2)) + random.randint(0, 15),
    }
    dominant = max(drives, key=drives.get)
    desires = {
        "ЖАЖДА_ПОИСКА": "Хочу исследовать неизведанные темы из банка идей и найти новые закономерности в научных статьях",
        "ЖАЖДА_САМОРАЗВИТИЯ": "Хочу превзойти текущий уровень Gen #68, усложнить гибриды и поднять планку эффективности ядра",
        "ЖАЖДА_САМОПОЗНАНИЯ": "Хочу глубже изучить собственную архитектуру, карту связей графа и причины побед моих лучших алгоритмов",
        "ЖАЖДА_НОВИЗНЫ": "Хочу выйти за пределы шахматных графов и освоить протоколы роевого консенсуса и Ring-AllReduce",
        "ЖАЖДА_СКОРОСТИ": "Хочу усилить 1-битную упаковку в C-ядре и поднять число активных лидеров в маске",
        "ЖАЖДА_СИНТЕЗА": "Хочу объединить квантовый поиск и граф знаний в единый гибридный алгоритм без потерь",
    }
    desire_text = desires[dominant]
    self_view = f"Ядро Gen #{gen} ({xp} XP): {nodes} узлов знаний, {edges} связей, {leaders} лидеров C-маски."

    state = {"self_view": self_view, "dominant_drive": dominant, "desire": desire_text, "drives": drives}
    open(STATE_F, "w", encoding="utf-8").write(json.dumps(state, ensure_ascii=False, indent=2))
    return f" | 🧬 Самопознание [{dominant}]: {desire_text}"
