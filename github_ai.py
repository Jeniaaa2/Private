
import time as _t
def _kg_hint():
    try:
        kg = _j.loads(open("knowledge_graph.json").read())
        import intrinsic_drive as _id
        return " | " + _id.reflect_and_desire().strip(" | ") + " | Граф: " + "; ".join([k for k, v in kg.get("strong_links", [])[:5]])
    except Exception:
        return ""
import json as _j
def _arbiter_mult():
    try: return float(_j.loads(open('agent_policy.json', encoding='utf-8').read()).get('last_mult', 1.0))
    except Exception: return 1.0

import os, re, time, json, random, urllib.request as ur

def _bench_plugin(fn_obj):
    sample = "Quantum graph compression 3-SAT LWE-32 lattice cryptography evolutionary search algorithms 2026"
    t0 = time.perf_counter()
    for _ in range(500):
        out = fn_obj(sample)
    dt = time.perf_counter() - t0
    if not isinstance(out, str) or len(out.strip()) < 25 or out.strip() == sample:
        return -1.0
    if dt > 0.08:
        return -1.0
    uniq = len(set(out.lower().split()))
    return round(uniq / max(dt, 1e-5), 1)

def _evolve_local_plugin(topic, intel, best_score, pdir):
    # Автономная эволюция кода плагина на основе лучших практик (precompiled regex + fast dict lookup)
    top_n = random.choice((6, 7, 8))
    sum_w = random.choice((30, 35, 40))
    code = f"""import re
from collections import Counter

_RX = re.compile(r'[^\w\s]')
_STOP = frozenset({"the","and","for","nor","but","a","an","of","in","on","to","from","by","with","that","this","is","are","как","для","или","при","что","это","без"})

def transform(text: str) -> str:
    words = [w for w in _RX.sub('', text.lower()).split() if len(w) > 3 and w not in _STOP]
    top_terms = [w for w, _ in Counter(words).most_common({top_n})]
    summary = ' '.join(text.split()[:{sum_w}])
    return "Ключевые термины: " + ", ".join(top_terms) + ". Сводка: " + summary
"""
    ns = {}
    exec(code, ns)
    cand_score = _bench_plugin(ns["transform"])
    if cand_score > best_score and cand_score > 0:
        pname = f"champ_{int(cand_score)}_{int(time.time())}.py"
        open(os.path.join(pdir, pname), "w", encoding="utf-8").write(code)
        all_p = sorted([f for f in os.listdir(pdir) if f.endswith(".py")])
        for old_p in all_p[:-3]:
            os.remove(os.path.join(pdir, old_p))
        return f" | 🏆 Evo-Code: новый плагин-чемпион {pname} (балл={cand_score} > {best_score})"
    return f" | 🛡️ Evo-Code: плагин проверен (балл={cand_score}, лидер={best_score})"


def _bench_math_plugin(fn_obj):
    import array as _ar
    arr = _ar.array('I', range(1, 4097))
    t0 = time.perf_counter()
    for _ in range(50):
        res = fn_obj(arr)
    dt = time.perf_counter() - t0
    if not isinstance(res, int) or res == 0 or dt > 0.15:
        return -1.0
    return round((4096 * 50) / max(dt, 1e-6), 1)

def evolve_numeric_plugin(topic):
    base = os.path.dirname(os.path.abspath(__file__))
    pdir = os.path.join(base, "ai_core_modules", "auto_plugins")
    os.makedirs(pdir, exist_ok=True)
    best_m = 0.0
    for fn in sorted([f for f in os.listdir(pdir) if f.startswith("math_") and f.endswith(".py")]):
        try:
            ns = {}
            exec(open(os.path.join(pdir, fn), encoding="utf-8").read(), ns)
            if "fast_math" in ns:
                sc = _bench_math_plugin(ns["fast_math"])
                if sc > best_m:
                    best_m = sc
        except Exception:
            pass

    shift_a = random.choice((5, 7, 11, 13))
    shift_b = random.choice((3, 9, 15, 17))
    mult_c = random.choice((2654435761, 2246822519, 3266489917))
    code = (
        "def fast_math(arr):\n"
        "    mv = memoryview(arr).cast('B').cast('Q')\n"
        "    acc = 0x9E3779B97F4A7C15\n"
        f"    for w in mv:\n"
        f"        acc ^= ((w << {shift_a}) ^ (w >> {shift_b})) * {mult_c} & 0xFFFFFFFFFFFFFFFF\n"
        "    return int(acc & 0xFFFFFFFF)\n"
    )
    ns = {}
    exec(code, ns)
    cand_m = _bench_math_plugin(ns["fast_math"])
    if cand_m > best_m and cand_m > 0:
        pname = f"math_champ_{int(cand_m // 1000)}k_{int(time.time())}.py"
        open(os.path.join(pdir, pname), "w", encoding="utf-8").write(code)
        all_m = sorted([f for f in os.listdir(pdir) if f.startswith("math_") and f.endswith(".py")])
        for old_m in all_m[:-3]:
            os.remove(os.path.join(pdir, old_m))
        return f" | 🧮 Числовой плагин {pname} принят ({int(cand_m):,} ops/s)"
    return f" | 🧮 Числовой лидер устоял ({int(best_m):,} ops/s)"

def ask_github_ai(topic, intel):
    base = os.path.dirname(os.path.abspath(__file__))
    pdir = os.path.join(base, "ai_core_modules", "auto_plugins")
    os.makedirs(pdir, exist_ok=True)

    best_score = 0.0
    for fn in sorted([f for f in os.listdir(pdir) if f.endswith(".py")]):
        try:
            ns = {}
            exec(open(os.path.join(pdir, fn), encoding="utf-8").read(), ns)
            if "transform" in ns:
                sc = _bench_plugin(ns["transform"])
                if sc > best_score:
                    best_score = sc
                ns["transform"](intel[:300])
        except Exception:
            pass

    prompt = (
        f"Тема: {topic}. Напиши: 1) Краткий научный вывод (3 предложения). "
        f"2) Быструю Python-функцию на стандартной библиотеке внутри ```python ... ``` с сигнатурой def transform(text: str) -> str:"
    )

    ans = ""
    src_name = ""
    endpoints = [
        ("https://models.inference.ai.://azure.com", "gpt-4o-mini", os.environ.get("GITHUB_TOKEN", "").strip(), "GitHub-AI"),
        ("https://text.pollinations.ai/openai", "openai", "", "OpenAI-Free")
    ]
    for url, mdl, tok, label in endpoints:
        try:
            hdrs = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
            if tok:
                hdrs["Authorization"] = f"Bearer {tok}"
            body = json.dumps({"model": mdl, "messages": [{"role": "user", "content": prompt}]}).encode()
            res = json.loads(ur.urlopen(ur.Request(url, data=body, headers=hdrs), timeout=25).read().decode())
            ans = next(iter(res.get("choices", ()))).get("message", {}).get("content", "").strip()
            if ans:
                src_name = label
                break
        except Exception:
            continue

    if ans:
        enc = os.path.join(base, "master_encyclopedia.md")
        with open(enc, "a", encoding="utf-8") as f:
            f.write(f"\n### [{src_name} Глубокий разбор: {topic}]\n{ans}\n")
        m = re.search(r"```python\s*(.*?)```", ans, re.S)
        if m:
            try:
                code = m.group(1).strip()
                compile(code, "<ai_candidate>", "exec")
                ns = {}
                exec(code, ns)
                cand_score = _bench_plugin(ns["transform"])
                if cand_score > best_score and cand_score > 0:
                    pname = f"champ_{int(cand_score)}_{int(time.time())}.py"
                    open(os.path.join(pdir, pname), "w", encoding="utf-8").write(code + "\n")
                    all_p = sorted([f for f in os.listdir(pdir) if f.endswith(".py")])
                    for old_p in all_p[:-3]:
                        os.remove(os.path.join(pdir, old_p))
                    return f" | 🏆 {src_name}: новый плагин {pname} (балл={cand_score})"
            except Exception:
                pass
        return f" | 🧠 {src_name}: разбор записан (лидер={best_score})" + evolve_numeric_plugin(topic)

    return _evolve_local_plugin(topic, intel, best_score, pdir) + evolve_numeric_plugin(topic)
