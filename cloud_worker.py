import os, re, json, time, random, zlib, gzip, subprocess
import urllib.request as ur, urllib.parse as up

GH_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
BRAIN_ZLIB = "compressed_brain.zlib"
EVO_LOG = "evolution_log.json"

def ask_cloud_ai(prompt, max_tok=420):
    if not GH_TOKEN:
        return ""
    try:
        url = "https://azure.com"
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tok,
            "temperature": 0.75
        }).encode("utf-8")
        req = ur.Request(url, data=payload, headers={
            "Authorization": f"Bearer {GH_TOKEN}",
            "Content-Type": "application/json"
        })
        resp = json.loads(ur.urlopen(req, timeout=30).read().decode("utf-8"))
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Cloud AI note:", e)
        return ""

def read_past_experience():
    if os.path.exists(BRAIN_ZLIB):
        try:
            lines = zlib.decompress(open(BRAIN_ZLIB, "rb").read()).decode("utf-8", "ignore").splitlines()
            return "\n".join(lines[-5:])[-800:]
        except Exception:
            pass
    return "Начальный этап: базовые алгоритмы графов, шахматной оценки и сжатия данных."

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
past = read_past_experience()
evo = json.loads(open(EVO_LOG, encoding="utf-8").read()) if os.path.exists(EVO_LOG) else {"gen": 0, "history": []}
gen = evo.get("gen", 0) + 1

# 1. Самостоятельная постановка новой цели на основе прошлых открытий из compressed_brain.zlib
goal_raw = ask_cloud_ai(
    f"Ты автономный саморазвивающийся ИИ (поколение #{gen}). Вот твои прошлые открытия из сжатой памяти:\n{past}\n"
    f"Придумай 1 НОВУЮ, более глубокую научную или алгоритмическую тему (из области шахматных алгоритмов, теории графов, криптоанализа, сжатия данных или ИИ), "
    f"которую нужно изучить следующей. Ответь строго в формате: ТЕМА_RU: <2-4 слова> | ТЕМА_EN: <2-4 слова на английском>",
    max_tok=90
)

m_ru = re.search(r"ТЕМА_RU:\s*([^|\n]+)", goal_raw)
m_en = re.search(r"ТЕМА_EN:\s*([^|\n]+)", goal_raw)
ru_q = m_ru.group(1).strip() if m_ru else random.choice(["Альфа-бета отсечение", "Алгоритм Хаффмана", "Криптография эллиптических кривых", "Поиск пути A*", "Генетические алгоритмы"])
en_q = m_en.group(1).strip() if m_en else "Alpha-beta pruning"

# 2. Сбор свежих данных из сети по самостоятельно выбранной теме
t_ru, s_ru = fetch_wiki("ru", ru_q)
t_en, s_en = fetch_wiki("en", en_q)
fact = s_ru or s_en or ru_q

# 3. Внутренние дебаты и генерация нового проверенного модуля на сервере GitHub
synthesis = ask_cloud_ai(
    f"Ты Стратег и Критик саморазвивающегося ИИ (Поколение #{gen}). Тема: '{ru_q}'. Теория из сети: {fact[:350]}. "
    f"1) Сформулируй главный инсайт (2 предложения на русском). "
    f"2) Напиши короткий рабочий Python-скрипт (10-18 строк, только стандартные библиотеки, без input), который моделирует этот алгоритм и печатает результат через print(), обернув код в ```python ... ```."
)

code_m = re.search(r"```python\s*(.*?)```", synthesis, re.S)
mod_status = "Теория усвоена"
if code_m:
    code_txt = code_m.group(1).strip()
    if not any(b in code_txt for b in ("os.system", "subprocess", "rm -rf", "input(")):
        os.makedirs("ai_core_modules", exist_ok=True)
        mod_name = f"ai_core_modules/evo_gen{gen}_{int(time.time())}.py"
        open(mod_name, "w", encoding="utf-8").write(f"# Auto-evolved Gen #{gen}: {ru_q}\n" + code_txt + "\n")
        r_test = subprocess.run(["python3", mod_name], capture_output=True, text=True, timeout=6)
        if r_test.returncode == 0 and r_test.stdout.strip():
            mod_status = f"Создан и проверен модуль {os.path.basename(mod_name)} -> {r_test.stdout.strip()[:90]}"
        else:
            os.remove(mod_name)

clean_note = re.sub(r"```python.*?```", "", synthesis, flags=re.S).strip()[:360] or fact[:360]
rec = f"[Эволюция Gen #{gen} | {now_s}] Тема: {ru_q} | {clean_note} | {mod_status}"

# 4. Сохранение в сжатый мозг zlib-9, текстовую базу и ленту пульта
with open("chat_knowledge.txt", "a", encoding="utf-8") as f:
    f.write(rec + "\n")
raw_b = zlib.decompress(open(BRAIN_ZLIB, "rb").read()) if os.path.exists(BRAIN_ZLIB) else b""
open(BRAIN_ZLIB, "wb").write(zlib.compress(raw_b + (rec + "\n").encode("utf-8"), level=9))

feed = json.loads(open("cloud_feed.json", encoding="utf-8").read()) if os.path.exists("cloud_feed.json") else []
feed.append({"src": f"Эволюция Gen #{gen}", "title": f"{ru_q} ({mod_status[:45]})", "info": clean_note, "time": now_s})
open("cloud_feed.json", "w", encoding="utf-8").write(json.dumps(feed[-60:], ensure_ascii=False, indent=2))

evo["gen"] = gen
evo["history"].append({"gen": gen, "topic": ru_q, "status": mod_status, "time": now_s})
open(EVO_LOG, "w", encoding="utf-8").write(json.dumps(evo[-50:], ensure_ascii=False, indent=2))
print(f"Evolution Gen #{gen} complete: {ru_q} | {mod_status}")
