import os, re, time, json, urllib.request as ur, subprocess

CLD = os.path.expanduser("~/ai_cloud")
MOD_DIR = os.path.join(CLD, "ai_core_modules")
os.makedirs(MOD_DIR, exist_ok=True)

def ask_local_llama(prompt):
    try:
        u = "http://127.0.0"
        payload = json.dumps({
            "model": "qwen",
            "messages": [
                {"role": "system", "content": "Ты генератор автономных Python-агентов. Отвечай ТОЛЬКО рабочим кодом Python внутри блока ```python ... ``` без лишних слов. Код должен использовать только стандартную библиотеку Python и печатать 1 строку результата."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 350
        }).encode("utf-8")
        req = ur.Request(u, data=payload, headers={"Content-Type": "application/json"})
        resp = json.loads(ur.urlopen(req, timeout=45).read().decode("utf-8"))
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ERR: {e}"

def spawn_on_llama():
    print("\033[96m=== РОЖДЕНИЕ АВТОНОМНОГО АГЕНТА НА БАЗЕ ЛОКАЛЬНОЙ LLAMA / QWEN ===\033[0m")
    topics = [
        "квантовая суперпозиция и интерференция амплитуд на 4 кубитах",
        "эвристическая оценка шахматной позиции по битовым маскам",
        "быстрое энтропийное сжатие и расчёт информационной плотности"
    ]
    topic = topics[int(time.time()) % len(topics)]
    print(f" * Задание для Qwen: {topic}")
    
    raw = ask_local_llama(f"Напиши короткий быстрый Python-скрипт на тему: {topic}. Выведи результат вычислений через print().")
    m = re.search(r"```python\s*(.*?)```", raw, re.S)
    code = m.group(1).strip() if m else ""
    
    ts = int(time.time())
    agent_name = f"llama_agent_{ts}.py"
    agent_path = os.path.join(MOD_DIR, agent_name)
    
    # Проверяем сгенерированный нейросетью код; если Llama была выключена или ошиблась — включаем страховку
    valid = False
    if code:
        open(agent_path, "w", encoding="utf-8").write(f"# Сгенерировано локальной Llama/Qwen | Тема: {topic}\n" + code + "\n")
        res = subprocess.run(["python", agent_path], capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            valid = True
            out = res.stdout.strip().splitlines()[-1]
            print(f"\033[92m[УСПЕХ! Нейросеть Qwen сама написала живого агента: {agent_name}]\033[0m")
            print(f" * Вывод агента: {out}")

    if not valid:
        fallback = (
            f"# Агент-резерв (Llama оффлайн) | Тема: {topic}\n"
            "import math, time\n"
            "t0 = time.perf_counter()\n"
            "vals = [math.sin(i * 0.37) ** 2 for i in range(64)]\n"
            "norm = round(sum(vals), 4)\n"
            "dt = round((time.perf_counter() - t0) * 1e6, 2)\n"
            f"print(f'Резервный агент [{topic}]: сумма_амплитуд={{norm}}, время={{dt}} мкс')\n"
        )
        open(agent_path, "w", encoding="utf-8").write(fallback)
        out = subprocess.run(["python", agent_path], capture_output=True, text=True).stdout.strip()
        print(f"\033[93m[Llama на порту 8080 не ответила -> создан резервный агент: {agent_name}]\033[0m")
        print(f" * Вывод агента: {out}")

    # Отправка нового агента в облако GitHub
    subprocess.run(["git", "-C", CLD, "pull", "--rebase", "--autostash"], capture_output=True)
    subprocess.run(["git", "-C", CLD, "add", "ai_core_modules"], capture_output=True)
    subprocess.run(["git", "-C", CLD, "commit", "-m", f"Spawn agent {agent_name} via local Llama/Qwen"], capture_output=True)
    push = subprocess.run(["git", "-C", CLD, "push"], capture_output=True, text=True)
    print("\033[96m[Облако GitHub]:\033[0m", "OK (Новый агент загружен в репозиторий)" if push.returncode == 0 else "Сохранено локально")

if __name__ == "__main__":
    spawn_on_llama()
