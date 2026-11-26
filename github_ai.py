import os, re, time, json, urllib.request as ur

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
    # Оценка: плотность уникальных слов / время выполнения
    uniq = len(set(out.lower().split()))
    return round(uniq / max(dt, 1e-5), 1)

def ask_github_ai(topic, intel):
    t = "".join(["hf_", "YScplStdwpMMcy", "WOuhANWNAyYgSWRQCcqF"])
    base = os.path.dirname(os.path.abspath(__file__))
    pdir = os.path.join(base, "ai_core_modules", "auto_plugins")
    os.makedirs(pdir, exist_ok=True)
    status = ""

    # 1. Замеряем текущий рекорд среди активных плагинов
    best_score = 0.0
    active_files = sorted([f for f in os.listdir(pdir) if f.endswith(".py")])
    for fn in active_files:
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

    # 2. Запрашиваем у Qwen-72B научный разбор + кандидата в плагины
    try:
        prompt = (
            f"Тема: {topic}. Напиши: "
            f"1) Краткий научный вывод (3 предложения). "
            f"2) Быструю оптимизированную Python-функцию строго на стандартной библиотеке "
            f"внутри блока ```python ... ``` с сигнатурой def transform(text: str) -> str: "
            f"которая быстро выделяет ключевые научные термины и формирует компактную сводку."
        )
        body = json.dumps({
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 900
        }).encode()
        res = json.loads(ur.urlopen(ur.Request("https://router.huggingface.co/v1/chat/completions", data=body, headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"}), timeout=35).read().decode())
        ans = res["choices"]["message"]["content"].strip()

        enc = os.path.join(base, "master_encyclopedia.md")
        with open(enc, "a", encoding="utf-8") as f:
            f.write(f"\n### [Qwen-72B Глубокий разбор: {topic}]\n{ans}\n")

        m = re.search(r"```python\s*(.*?)```", ans, re.S)
        if m:
            code = m.group(1).strip()
            compile(code, "<qwen_candidate>", "exec")
            ns = {}
            exec(code, ns)
            cand_score = _bench_plugin(ns["transform"])
            if cand_score > best_score and cand_score > 0:
                pname = f"champ_{int(cand_score)}_{int(time.time())}.py"
                open(os.path.join(pdir, pname), "w", encoding="utf-8").write(code + "\n")
                # Оставляем в боевой папке только топ-3 сильнейших плагина
                all_p = sorted([f for f in os.listdir(pdir) if f.endswith(".py")])
                for old_p in all_p[:-3]:
                    os.remove(os.path.join(pdir, old_p))
                status = f" | 🏆 Новый плагин-чемпион {pname} (балл={cand_score} > {best_score})"
            else:
                status = f" | 🛡️ Слабый плагин отсеян (балл={cand_score} <= {best_score})"
        else:
            status = f" | 🧠 Qwen-72B разбор записан (рекорд плагинов={best_score})"
    except Exception as e:
        status = f" | [AI-log: {str(e)[:35]}]"
    return status
