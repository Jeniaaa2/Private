import os, re, json, time, random, zlib, gzip
import urllib.request as ur, urllib.parse as up

# Использует встроенный GITHUB_TOKEN серверов GitHub Actions (без регистраций и ключей!)
GH_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

TOPICS = [
    ("autonomous ai agents", "Автономные ИИ-агенты"),
    ("chess engine evaluation", "Шахматные движки и оценка"),
    ("cryptography hash algorithms", "Криптография и защита"),
    ("graph shortest path", "Оптимизация графов"),
    ("quantum computing", "Квантовые вычисления"),
    ("data compression algorithms", "Алгоритмы сжатия данных")
]

def ask_github_ai(prompt):
    if not GH_TOKEN:
        return ""
    try:
        url = "https://azure.com"
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 350,
            "temperature": 0.7
        }).encode("utf-8")
        req = ur.Request(url, data=payload, headers={
            "Authorization": f"Bearer {GH_TOKEN}",
            "Content-Type": "application/json"
        })
        resp = json.loads(ur.urlopen(req, timeout=25).read().decode("utf-8"))
        return resp["choices"]["message"]["content"].strip()
    except Exception as e:
        print("GitHub Models note:", e)
        return ""

def fetch_wiki(lang, q):
    try:
        u1 = f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={up.quote(q)}&format=json&srlimit=1"
        r1 = ur.urlopen(ur.Request(u1, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}), timeout=10)
        raw1 = gzip.decompress(r1.read()) if r1.info().get("Content-Encoding") == "gzip" else r1.read()
        hit = next(iter(json.loads(raw1.decode("utf-8", "ignore")).get("query", {}).get("search", [])), None)
        if not hit: return "", ""
        title = hit.get("title", "")
        u2 = f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles={up.quote(title)}&format=json"
        r2 = ur.urlopen(ur.Request(u2, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}), timeout=10)
        raw2 = gzip.decompress(r2.read()) if r2.info().get("Content-Encoding") == "gzip" else r2.read()
        page = next(iter(json.loads(raw2.decode("utf-8", "ignore")).get("query", {}).get("pages", {}).values()), {})
        sents = [x.strip() for x in " ".join(page.get("extract", "").split()).split(". ") if len(x.strip()) > 35][:3]
        return title, ". ".join(sents)[:550]
    except Exception:
        return "", ""

now_s = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
feed = json.loads(open("cloud_feed.json", encoding="utf-8").read()) if os.path.exists("cloud_feed.json") else []

en_q, ru_q = random.choice(TOPICS)
t_ru, s_ru = fetch_wiki("ru", ru_q)
t_en, s_en = fetch_wiki("en", en_q)
fact = s_ru or s_en or ru_q

ai_thought = ask_github_ai(
    f"Ты команда ИИ (Стратег и Критик) на облачном сервере. Тема: '{ru_q}'. "
    f"Данные из сети: {fact[:300]}. "
    f"Выдайте короткий глубокий спор (2 фразы: Стратег предлагает архитектурную идею, Критик называет главный риск и способ проверки) на русском."
)

if ai_thought:
    rec = f"[GitHub-AI Облако {now_s}] ({ru_q}) {ai_thought}"
    feed.append({"src": "GitHub AI (Облако)", "title": ru_q, "info": ai_thought[:450], "time": now_s})
elif fact:
    rec = f"[Облачный Бот {now_s}] ({ru_q}) {t_ru}: {fact}"
    feed.append({"src": "Облако GitHub", "title": t_ru or ru_q, "info": fact[:450], "time": now_s})
else:
    rec = ""

if rec:
    with open("chat_knowledge.txt", "a", encoding="utf-8") as f:
        f.write(rec + "\n")
    raw_b = zlib.decompress(open("compressed_brain.zlib", "rb").read()) if os.path.exists("compressed_brain.zlib") else b""
    open("compressed_brain.zlib", "wb").write(zlib.compress(raw_b + (rec + "\n").encode("utf-8"), level=9))

open("cloud_feed.json", "w", encoding="utf-8").write(json.dumps(feed[-60:], ensure_ascii=False, indent=2))
print("GitHub Models cycle done.")
