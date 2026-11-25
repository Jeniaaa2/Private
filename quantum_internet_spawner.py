import os, re, time, json, math, urllib.request as ur, urllib.parse as up, subprocess

CLD = os.path.expanduser("~/ai_cloud")
MOD_DIR = os.path.join(CLD, "ai_core_modules")
os.makedirs(MOD_DIR, exist_ok=True)

def fetch_science_seed():
    queries = ["quantum+walk+graph", "quantum+fourier+transform", "grover+search+algorithm", "bell+entanglement"]
    q = queries[int(time.time()) % len(queries)]
    titles = []
    # 1. Выход в интернет: OpenAlex API
    try:
        u1 = f"https://openalex.org{q}&per-page=2"
        req1 = ur.Request(u1, headers={"User-Agent": "QuantumSpawner/1.0"})
        data1 = json.loads(ur.urlopen(req1, timeout=10).read().decode("utf-8", "ignore"))
        for item in data1.get("results", []):
            if item.get("title"):
                titles.append(item.get("title")[:85])
    except Exception:
        pass
    # 2. Выход в интернет: arXiv API
    try:
        u2 = f"http://arxiv.org:{q}&max_results=2"
        xml = ur.urlopen(u2, timeout=10).read().decode("utf-8", "ignore")
        for m in re.findall(r"<title>(.*?)</title>", xml, re.S)[1:]:
            clean_t = " ".join(m.split())[:85]
            if clean_t:
                titles.append(clean_t)
    except Exception:
        pass
    return q.replace("+", " "), titles or ["Quantum Superposition & Graph Interference"]

def spawn_agent(count=2):
    print("\033[96m=== ЗАПУСК КВАНТОВОГО ИНКУБАТОРА АГЕНТОВ (ИНТЕРНЕТ -> ТЕРМУКС -> ОБЛАКО) ===\033[0m")
    for idx in range(1, count + 1):
        topic, articles = fetch_science_seed()
        seed = sum(ord(c) for c in "".join(articles)) + int(time.time()) + idx
        n_qubits = 4 + (seed % 3)  # 4, 5 или 6 кубитов (16, 32 или 64 состояния)
        dim = 1 << n_qubits
        target = seed % dim
        agent_id = f"q_agent_{int(time.time())}_{idx}"
        agent_path = os.path.join(MOD_DIR, f"{agent_id}.py")

        code = (
            f"# Автономный квантовый микро-агент: {agent_id}\n"
            f"# Источники из интернета: {' | '.join(articles)[:140]}\n"
            "import math, cmath, time\n"
            f"TOPIC = {topic!r}\n"
            f"N_QUBITS, DIM, TARGET = {n_qubits}, {dim}, {target}\n"
            "t0 = time.perf_counter()\n"
            "inv_s = 1.0 / math.sqrt(DIM)\n"
            "state = {i: complex(inv_s, 0.0) for i in range(DIM)}\n"
            "iters = max(1, int((math.pi / 4.0) * math.sqrt(DIM)))\n"
            "for _ in range(iters):\n"
            "    state[TARGET] = -state.get(TARGET, 0j)\n"
            "    mean_a = sum(state.values()) / DIM\n"
            "    state = {i: 2.0 * mean_a - amp for i, amp in state.items()}\n"
            "probs = {i: abs(amp) ** 2 for i, amp in state.items()}\n"
            "p_hit = round(probs.get(TARGET, 0.0) * 100.0, 2)\n"
            "entropy = round(-sum(p * math.log2(p) for p in probs.values() if p > 1e-12), 4)\n"
            "dt = round((time.perf_counter() - t0) * 1e6, 2)\n"
            "print(f'[{TOPIC}] Кубитов={N_QUBITS} ({DIM} сост.) | Цель |{TARGET:0{N_QUBITS}b}> P={p_hit}% | H_q={entropy} бит | {dt} мкс')\n"
        )
        open(agent_path, "w", encoding="utf-8").write(code)
        out = subprocess.run(["python", agent_path], capture_output=True, text=True).stdout.strip()
        print(f"\n\033[92m[Рождён агент #{idx}: {agent_id}.py]\033[0m")
        print(f" * Найдено в интернете: {articles[0]}")
        print(f" * Живая работа агента: {out}")
        time.sleep(1)

    # Синхронизация новых агентов с облаком GitHub
    subprocess.run(["git", "-C", CLD, "pull", "--rebase", "--autostash"], capture_output=True)
    subprocess.run(["git", "-C", cld if 'cld' in globals() else CLD, "add", "ai_core_modules"], capture_output=True)
    subprocess.run(["git", "-C", CLD, "commit", "-m", f"Spawn {count} quantum internet micro-agents from Termux"], capture_output=True)
    push = subprocess.run(["git", "-C", CLD, "push"], capture_output=True, text=True)
    print("\n\033[93m[Синхронизация с облаком GitHub]:\033[0m", "OK (Агенты ушли в облако)" if push.returncode == 0 else "Сохранено локально")

if __name__ == "__main__":
    spawn_agent(2)
