import os, json, time, math, cmath, random, glob, subprocess

CLD = os.path.expanduser("~/ai_cloud")
MOD_DIR = os.path.join(CLD, "ai_core_modules")
ARCH_DIR = os.path.join(MOD_DIR, "archive")
GENOME_PATH = os.path.join(CLD, "genome.json")
os.makedirs(ARCH_DIR, exist_ok=True)

def load_genome():
    if os.path.exists(GENOME_PATH):
        try:
            return json.loads(open(GENOME_PATH, encoding="utf-8").read())
        except Exception:
            pass
    return {"qubits": 5, "depth": 6, "alpha_gain": 1.0, "record_ops": 1000, "champions": 0}

def run_darwin_crossover(gen_num, topic_name, seed_val):
    g = load_genome()
    rng = random.Random(seed_val + gen_num * 31)

    # 1. Мутация генов (выбор оптимальных параметров потомка)
    mut_qubits = max(4, min(7, g.get("qubits", 5) + rng.choice((-1, 0, 1))))
    mut_depth = max(4, min(8, g.get("depth", 6) + rng.choice((-1, 0, 1))))
    mut_gain = round(max(0.85, min(1.25, g.get("alpha_gain", 1.0) + rng.uniform(-0.08, 0.08))), 3)

    dim = 1 << mut_qubits
    target = (seed_val + gen_num) % dim
    iters = max(1, int((math.pi / 4.0) * math.sqrt(dim) * mut_gain))

    # 2. Скрещивание: Квантовый поиск Гровера + 64-битный Шахматный Bitboard
    hybrid_name = f"hybrid_gen{gen_num}_{int(time.time())}.py"
    hybrid_path = os.path.join(MOD_DIR, hybrid_name)

    code = (
        f"# 🧬 ДАРВИНОВСКИЙ ГИБРИД ПОКОЛЕНИЯ Gen #{gen_num}: Квантовый Гровер ({mut_qubits}q) x Bitboard 8x8\n"
        f"# Тема эволюции: {topic_name}\n"
        "import math, time, random\n"
        f"QUBITS, DIM, TARGET, ITERS, DEPTH = {mut_qubits}, {dim}, {target}, {iters}, {mut_depth}\n"
        "t0 = time.perf_counter()\n"
        "# Фаза I: Квантовая суперпозиция и усиление амплитуд Гровера\n"
        "inv_s = 1.0 / math.sqrt(DIM)\n"
        "state = {i: complex(inv_s, 0.0) for i in range(DIM)}\n"
        "for _ in range(ITERS):\n"
        "    state[TARGET] = -state.get(TARGET, 0j)\n"
        "    mean_a = sum(state.values()) / DIM\n"
        "    state = {i: 2.0 * mean_a - amp for i, amp in state.items()}\n"
        "best_q = max(state, key=lambda k: abs(state.get(k, 0j)) ** 2)\n"
        "p_q = round((abs(state.get(best_q, 0j)) ** 2) * 100.0, 2)\n"
        "# Фаза II: Тактический 64-битный Bitboard-анализ по квантовому ключу\n"
        "random.seed(best_q + DEPTH)\n"
        "board = random.getrandbits(64)\n"
        "not_a, not_h = 0xfefefefefefefefe, 0x7f7f7f7f7f7f7f7f\n"
        "attacks = ((board & not_h) << 1) | ((board & not_a) >> 1) | (board << 8) | (board >> 8)\n"
        "attacks &= 0xffffffffffffffff\n"
        "dt = round((time.perf_counter() - t0) * 1e6, 2)\n"
        "print(f'Гибрид [Гровер {QUBITS}q x Bitboard]: ветка=|{best_q:0{QUBITS}b}> (P={p_q}%), битых_полей={attacks.bit_count()}, время={dt} мкс')\n"
    )
    open(hybrid_path, "w", encoding="utf-8").write(code)

    # 3. Честный турнир в памяти (500 прогонов скомпилированного байт-кода без накладных расходов процесса)
    import io, contextlib
    try:
        compiled = compile(code, hybrid_path, "exec")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compiled, {})
        last_out = buf.getvalue().strip()
        t_b0 = time.perf_counter()
        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull):
            for _ in range(500):
                exec(compiled, {})
        avg_us = max(1.0, ((time.perf_counter() - t_b0) / 500.0) * 1e6)
    except Exception:
        if os.path.exists(hybrid_path):
            os.remove(hybrid_path)
        return "Отбракован в турнире (сбой мутации)"
    ops_sec = int(1_000_000 / avg_us)
    old_rec = g.get("record_ops", 1000)

    # 4. Естественный отбор и обновление генома genome.json
    if ops_sec >= int(old_rec * 0.85):
        g["qubits"] = mut_qubits
        g["depth"] = mut_depth
        g["alpha_gain"] = mut_gain
        g["record_ops"] = max(old_rec, ops_sec)
        g["champions"] = g.get("champions", 0) + 1
        open(GENOME_PATH, "w", encoding="utf-8").write(json.dumps(g, ensure_ascii=False, indent=2))
        status = f"🧬 МУТАНТ-ЧЕМПИОН #{g['champions']} ({ops_sec} ops/s, гены: {mut_qubits}q/d{mut_depth})"
    else:
        os.replace(hybrid_path, os.path.join(ARCH_DIR, hybrid_name))
        status = f"Слабый мутант убран в архив ({ops_sec} < {old_rec} ops/s)"

    # Умная очистка активного ядра (держим максимум 16 элитных модулей)
    all_mods = sorted(glob.glob(os.path.join(MOD_DIR, "*.py")), key=os.path.getmtime)
    if len(all_mods) > 16:
        for old_m in all_mods[:-16]:
            os.replace(old_m, os.path.join(ARCH_DIR, os.path.basename(old_m)))

    return f"{status} | {last_out}"
