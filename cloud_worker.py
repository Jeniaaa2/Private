import os, re, json, time, random, zlib, gzip
import urllib.request as ur, urllib.parse as up

TOPICS = [
    ("autonomous ai agents", "Автономные ИИ-агенты"),
    ("chess engine evaluation", "Шахматные движки"),
    ("cryptography hash algorithms", "Криптография"),
    ("graph shortest path", "Теория графов"),
    ("quantum computing", "Квантовые вычисления"),
    ("data compression algorithms", "Сжатие данных")
]

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

en_q, ru_q = random.choice(TOPICS)
t_ru, s_ru = fetch_wiki("ru", ru_q)
t_en, s_en = fetch_wiki("en", en_q)
now_s = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())

if s_ru or s_en:
    rec = f"[GitHub-Сервер {now_s}] ({ru_q}) {t_ru}: {s_ru} | {t_en}: {s_en}"
    with open("chat_knowledge.txt", "a", encoding="utf-8") as f:
        f.write(rec + "\n")
    raw_b = zlib.decompress(open("compressed_brain.zlib", "rb").read()) if os.path.exists("compressed_brain.zlib") else b""
    open("compressed_brain.zlib", "wb").write(zlib.compress(raw_b + (rec + "\n").encode("utf-8"), level=9))
    print("OK:", rec[:120])
