import os, json

BASE = os.path.dirname(os.path.abspath(__file__))
LOG_F = os.path.join(BASE, "evolution_log.json")
GRAPH_F = os.path.join(BASE, "knowledge_graph.json")

def rebuild_graph():
    nodes, edges = {}, {}
    if os.path.exists(LOG_F):
        try:
            hist = json.loads(open(LOG_F, encoding="utf-8").read()).get("history", [])
            prev_topic = None
            for h in hist:
                t = h.get("topic", "Core")
                v = h.get("verdict", "")
                nodes[t] = nodes.get(t, 0) + 1
                if prev_topic and prev_topic != t:
                    pair = f"{prev_topic} -> {t}"
                    edges[pair] = edges.get(pair, 0) + 1
                for alg in ("Zobrist", "Quantum Walk", "QFT", "Bell", "LWE-32", "Хаффман"):
                    if alg in v:
                        link = f"{t} <=> {alg}"
                        edges[link] = edges.get(link, 0) + 1
                prev_topic = t
        except Exception:
            pass
    g = {"total_nodes": len(nodes), "total_edges": len(edges), "top_nodes": sorted(nodes.items(), key=lambda x: -x[1])[:8], "strong_links": sorted(edges.items(), key=lambda x: -x[1])[:12]}
    open(GRAPH_F, "w", encoding="utf-8").write(json.dumps(g, ensure_ascii=False, indent=2))
    return f" | 🕸️ Граф знаний: {len(nodes)} узлов, {len(edges)} связей"
