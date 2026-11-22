import urllib.request as ur, urllib.parse as up, json, random, os, re, subprocess, time, xml.etree.ElementTree as ET

MEM = "chat_knowledge.txt"
IDEAS = "ai_ideas.txt"
VIS = "visited_topics.txt"
os.makedirs("ai_core_modules", exist_ok=True)
os.makedirs("ai_sandbox", exist_ok=True)

for f in [MEM, IDEAS, VIS]:
    if not os.path.exists(f):
        open(f, "w", encoding="utf-8").write("")

def cloud_ai(prompt):
    # Используем бесплатный открытый облачный шлюз без ключей для серверных агентов
    try:
        u = "https://pollinations.ai" + up.quote(prompt[:900])
        req = ur.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        return ur.urlopen(req, timeout=25).read().decode("utf-8", "ignore").strip()
    except Exception as e:
        return ""

# 1. Выбор новой уникальной темы с научного сервера arXiv
vis = [v.lower() for v in open(VIS, encoding="utf-8").read().splitlines()]
topic = f"Quantum Algorithms {random.randint(100,999)}"
try:
    cat = random.choice(["cs.AI", "cs.CR", "cs.DS", "quant-ph", "math.CO"])
    u_ax = f"http://arxiv.org:{cat}&start={random.randint(0,100)}&max_results=10"
    rt = ET.fromstring(ur.urlopen(ur.Request(u_ax, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read())
    ns = {"a": "http://w3.org"}
    for e in rt.findall("a:entry", ns):
        words = [w for w in re.sub(r"[^a-zA-Z\s]", "", e.find("a:title", ns).text or "").split() if len(w) > 4]
        if len(words) >= 2:
            cand = " ".join(words[:2])
            if cand.lower() not in vis:
                topic = cand
                break
except Exception:
    pass

open(VIS, "a", encoding="utf-8").write(topic + "\n")
print(f"[Сервер-Разведчик] Новая цель: {topic}")

# 2. Сбор данных с серверов GitHub и arXiv
intel = []
try:
    u_gh = "https://github.com?" + up.urlencode({"q": topic, "sort": "stars", "per_page": 2})
    items = json.loads(ur.urlopen(ur.Request(u_gh, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read()).get("items", [])
    if items:
        intel.append("GitHub: " + "; ".join([f"{i['full_name']} ({i.get('description','')})" for i in items]))
except Exception:
    pass

# 3. Аналитик записывает вывод в облачную память
summary = cloud_ai(f"Напиши 1 глубокий практический вывод на русском (2 предложения) по теме '{topic}'. Данные: {' '.join(intel)}")
if summary and len(summary) > 20:
    open(MEM, "a", encoding="utf-8").write(f"[Сервер: {topic}] {summary}\n")
    print(f"[Сервер-Аналитик] Вывод сохранён: {summary[:90]}...")

# 4. Самопишущий Конструктор создаёт и проверяет свой новый модуль на сервере
code_raw = cloud_ai(f"Напиши ТОЛЬКО рабочий код Python без пояснений и без markdown-кавычек (стандартные модули, без input, с print() в конце) реализующий алгоритм по теме: {topic}")
code_clean = re.sub(r"^```python|```$", "", code_raw, flags=re.M).strip()
if code_clean and "print" in code_clean:
    fn = f"ai_core_modules/cloud_mod_{int(time.time())}.py"
    open(fn, "w", encoding="utf-8").write(code_clean)
    r = subprocess.run(["python3", fn], capture_output=True, text=True, timeout=10)
    if r.returncode == 0 and r.stdout.strip():
        open(MEM, "a", encoding="utf-8").write(f"[Сервер-Модуль {fn}] -> {r.stdout.strip()[:90]}\n")
        print(f"[Сервер-Конструктор] УСПЕХ! Модуль {fn} проверен на сервере: {r.stdout.strip()[:60]}")
    else:
        os.remove(fn)

# 5. Инноватор скрещивает накопленные знания
lines = [l.strip() for l in open(MEM, encoding="utf-8") if len(l.strip()) > 30]
if len(lines) >= 2:
    f1, f2 = random.sample(lines[-10:], 2)
    idea = cloud_ai(f"Объедини два факта и придумай 1 оригинальную инженерную идею на русском (2 предложения):\n1) {f1[:140]}\n2) {f2[:140]}")
    if idea and len(idea) > 25:
        open(IDEAS, "a", encoding="utf-8").write(f"[{time.strftime('%Y-%m-%d %H:%M')}] {idea}\n\n")
        print(f"[Сервер-Инноватор] Новая идея записана в облако!")
