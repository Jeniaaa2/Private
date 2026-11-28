import os, json, re

BASE = os.path.dirname(os.path.abspath(__file__))
LOG_F = os.path.join(BASE, "evolution_log.json")
GRAPH_F = os.path.join(BASE, "knowledge_graph.json")

def rebuild_graph():
    nodes, edges = {}, {}
    if os.path.exists(LOG_F):
        hist = json.loads(open(LOG_F, encoding="utf-8").read()).get("history", [])
        prev = None
        for h in hist:
            t, v = h.get("topic", "Core"), h.get("verdict", "")
            nodes[t] = nodes.get(t, 0) + 1
            w = 10 + (40 if "+40 XP" in v else 0) + (15 if "Попытка #1" in v else 0)
            m = re.search(r"([\d,]+)\s*ops/s", v)
            if m:
                w += int(m.group(1).replace(",", "")) // 10000000
            if prev and prev != t:
                k = f"{prev} -> {t}"
                edges[k] = edges.get(k, 0) + w
            for alg in ("Zobrist", "Quantum Walk", "QFT", "Bell", "LWE-32", "Хаффман", "Гровера", "MCTS"):
                if alg in v:
                    k = f"{t} <=> {alg}"
                    edges[k] = edges.get(k, 0) + w
            prev = t
    top_n = sorted(nodes.items(), key=lambda x: -x[1])[:8]
    top_e = sorted(edges.items(), key=lambda x: -x[1])[:12]
    g = {"total_nodes": len(nodes), "total_edges": len(edges), "top_nodes": top_n, "strong_links": top_e}
    open(GRAPH_F, "w", encoding="utf-8").write(json.dumps(g, ensure_ascii=False, indent=2))
    return f" | 🕸️ Граф знаний: {len(nodes)} узлов, {len(edges)} связей (топ-рейтинг={top_e[0][1] if top_e else 0})"
