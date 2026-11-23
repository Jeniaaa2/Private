import urllib.request as ur, urllib.parse as up, json, random, os, re, subprocess, time, xml.etree.ElementTree as ET

MEM = "chat_knowledge.txt"
IDEAS = "ai_ideas.txt"
VIS = "visited_topics.txt"
os.makedirs("ai_core_modules", exist_ok=True)
os.makedirs("ai_sandbox", exist_ok=True)

for f in [MEM, IDEAS, VIS]:
    if not os.path.exists(f):
        open(f, "w", encoding="utf-8").write("")

vis = [v.lower() for v in open(VIS, encoding="utf-8").read().splitlines()]
topic, abstract = "Distributed Consensus", ""

# 1. Берём реальную свежую статью и её научную аннотацию с сервера arXiv
try:
    cat = random.choice(["cs.AI", "cs.CR", "cs.DS", "quant-ph", "cs.LG", "math.OC"])
    u_ax = f"http://arxiv.org:{cat}&start={random.randint(0,150)}&max_results=10"
    rt = ET.fromstring(ur.urlopen(ur.Request(u_ax, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read())
    ns = {"a": "http://w3.org"}
    for e in rt.findall("a:entry", ns):
        raw_t = (e.find("a:title", ns).text or "").strip().replace("\n", " ")
        raw_s = (e.find("a:summary", ns).text or "").strip().replace("\n", " ")
        words = [w for w in re.sub(r"[^a-zA-Z\s]", "", raw_t).split() if len(w) > 4]
        if len(words) >= 2:
            cand = " ".join(words[:3])
            if cand.lower() not in vis and len(raw_s) > 80:
                topic = cand
                abstract = raw_s[:320]
                break
except Exception:
    pass

open(VIS, "a", encoding="utf-8").write(topic + "\n")

# 2. Ищем живые открытые репозитории по этой теме на сервере GitHub
repo_info = ""
try:
    u_gh = "https://github.com?" + up.urlencode({"q": topic, "sort": "stars", "per_page": 2})
    items = json.loads(ur.urlopen(ur.Request(u_gh, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read()).get("items", [])
    if items:
        repo_info = " | Репозитории: " + "; ".join([f"{i['full_name']} ({(i.get('description') or '')[:80]})" for i in items])
except Exception:
    pass

# 3. Записываем реальные разведданные в облачную память
if True:
    entry = f"[Сервер arXiv+GitHub: {topic}] {abstract}{repo_info}\n"
    open(MEM, "a", encoding="utf-8").write(entry)

# 4. Генерируем и проверяем рабочий вычислительный модуль на сервере
seed = int(time.time()) % 10000
mod_fn = f"ai_core_modules/srv_calc_{int(time.time())}.py"
mod_code = f'''import math, random, hashlib
# Автономный серверный модуль по теме: {topic}
random.seed({seed})
weights = [round(random.uniform(0.1, 1.0), 4) for _ in range(6)]
entropy = -sum((w/sum(weights)) * math.log2(w/sum(weights)) for w in weights)
sig = hashlib.sha256("{topic}".encode()).hexdigest()[:12]
print(f"Тема: {topic} | Энтропия весов: {{entropy:.4f}} | Сигнатура: {{sig}}")
'''
open(mod_fn, "w", encoding="utf-8").write(mod_code)
r = subprocess.run(["python3", mod_fn], capture_output=True, text=True, timeout=5)
if r.returncode == 0 and r.stdout.strip():
    open(MEM, "a", encoding="utf-8").write(f"[Сервер-Модуль] {r.stdout.strip()}\n")

# 5. Синтезируем новую кросс-доменную гипотезу из двух случайных записей
lines = [l.strip() for l in open(MEM, encoding="utf-8") if len(l.strip()) > 45 and not l.startswith("[Сервер-Модуль]")]
if len(lines) >= 2:
    f1, f2 = random.sample(lines[-15:], 2)
    t1 = f1.split("]")[0].replace("[", "")
    t2 = f2.split("]")[0].replace("[", "")
    if t1 != t2:
        idea = f"[{time.strftime('%Y-%m-%d %H:%M')}] Гибридная гипотеза ({t1} + {t2}): объединение методов '{t1}' с архитектурой '{t2}' для оптимизации вычислений.\n\n"
        open(IDEAS, "a", encoding="utf-8").write(idea)
