import os, re, json, time, random, zlib, gzip, subprocess, concurrent.futures
import urllib.request as ur, urllib.parse as up

GH_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
BRAIN_ZLIB = "compressed_brain.zlib"
EVO_LOG = "evolution_log.json"

def ask_cloud_ai(prompt, max_tok=450):
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
            return "\n".join(lines[-6:])[-900:]
        except Exception:
            pass
    return "Стартовая база: теория графов, шахматные эвристики, сжатие данных и криптоанализ."

def fetch_url(url):
    req = ur.Request(url, headers={"User-Agent": "Mozilla/5.0 (ResearchBot/2.0)", "Accept-Encoding": "gzip"})
    resp = ur.urlopen(req, timeout=10)
    raw = resp.read()
    if resp.info().get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "ignore")

# Паук 1: Научные препринты arXiv.org
def spider_arxiv(q):
    try:
        u = f"http://arxiv.org:{up.quote(q)}&max_results=2&sortBy=relevance"
        xml = fetch_url(u)
        titles = re.findall(r"<title>(.*?)</title>", xml, flags=re.S)
        summaries = re.findall(r"<summary>(.*?)</summary>", xml, flags=re.S)
        if len(titles) > 1 and summaries:
            t = " ".join(titles[1].split())[:90]
            s = " ".join(summaries[0].split())[:350]
            return f"[arXiv Наука] {t}: {s}"
    except Exception:
        pass
    return ""

# Паук 2: Мировая научная база OpenAlex (рецензируемые статьи)
def spider_openalex(q):
    try:
        u = f"https://openalex.org{up.quote(q)}&per-page=1&sort=cited_by_count:desc"
        data = json.loads(fetch_url(u))
        w = next(iter(data.get("results", [])), None)
        if w:
            title = w.get("title", "")[:90]
            year = w.get("publication_year", "")
            cites = w.get("cited_by_count", 0)
            return f"[OpenAlex Наука, {year}, цитирований: {cites}] {title}"
    except Exception:
        pass
    return ""

# Пауки 3 и 4: Wikipedia RU и Wikipedia EN
def spider_wiki(lang, q):
    try:
        u1 = f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={up.quote(q)}&format=json&srlimit=1"
        hit = next(iter(json.loads(fetch_url(u1)).get("query", {}).get("search", [])), None)
        if not hit: return ""
        title = hit.get("title", "")
        u2 = f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles={up.quote(title)}&format=json"
        pages = json.loads(fetch_url(u2)).get("query", {}).get("pages", {})
        page = next(iter(pages.values()), {})
        sents = [x.strip() for x in " ".join(page.get("extract", "").split()).split(". ") if len(x.strip()) > 35][:2]
        txt = ". ".join(sents)[:350]
        return f"[Wiki {lang.upper()}] {title}: {txt}" if txt else ""
    except Exception:
        pass
    return ""

now_s = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
past = read_past_experience()
evo = json.loads(open(EVO_LOG, encoding="utf-8").read()) if os.path.exists(EVO_LOG) else {"gen": 0, "history": []}
gen = evo.get("gen", 0) + 1

# 1. Стратегическое принятие решения: ИИ сам выбирает следующую цель на основе сжатой памяти
goal_raw = ask_cloud_ai(
    f"Ты быстрый саморазвивающийся ИИ-стратег (Поколение #{gen}). Прошлый опыт из памяти:\n{past}\n"
    f"Выбери 1 НОВУЮ научную тему на стыке алгоритмов, ИИ, шахматной оценки, графов или криптоанализа, чтобы закрыть пробелы в знаниях. "
    f"Ответь строго в формате: ТЕМА_RU: <2-4 слова> | ТЕМА_EN: <2-4 слова на английском>",
    max_tok=90
)

m_ru = re.search(r"ТЕМА_RU:\s*([^|\n]+)", goal_raw)
m_en = re.search(r"ТЕМА_EN:\s*([^|\n]+)", goal_raw)
ru_q = m_ru.group(1).strip() if m_ru else random.choice(["Монте-Карло поиск в дереве", "Нейроморфные вычисления", "Энтропийное кодирование", "Алгоритм Дейкстры с эвристикой", "Обучение с подкреплением"])
en_q = m_en.group(1).strip() if m_en else "Monte Carlo tree search"

# 2. Параллельный запуск 4 научных пауков одновременно (занимает ~2 секунды!)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    futures = [
        ex.submit(spider_arxiv, en_q),
        ex.submit(spider_openalex, en_q),
        ex.submit(spider_wiki, "ru", ru_q),
        ex.submit(spider_wiki, "en", en_q)
    ]
    intel_list = [f.result() for f in futures if f.result()]

combined_intel = " || ".join(intel_list) if intel_list else ru_q

# 3. Глубокий синтез 4 научных источников + создание и проверка нового модуля
synthesis = ask_cloud_ai(
    f"Ты саморазвивающийся ИИ (Поколение #{gen}). Тема: '{ru_q}'. "
    f"Данные от 4 научных пауков (arXiv, OpenAlex, Wiki RU/EN):\n{combined_intel[:900]}\n"
    f"1) Сделай острый практический вывод, объединяющий эти источники (2-3 предложения на русском). "
    f"2) Напиши рабочий Python-скрипт (12-18 строк, только стандартные библиотеки, без input), реализующий эту идею и печатающий итог через print(), в блоке ```python ... ```."
)

code_m = re.search(r"```python\s*(.*?)```", synthesis, re.S)
mod_status = f"Изучено {len(intel_list)} науч. источника"
if code_m:
    code_txt = code_m.group(1).strip()
    if not any(b in code_txt for b in ("os.system", "subprocess", "rm -rf", "input(")):
        os.makedirs("ai_core_modules", exist_ok=True)
        mod_name = f"ai_core_modules/evo_gen{gen}_{int(time.time())}.py"
        open(mod_name, "w", encoding="utf-8").write(f"# Auto-evolved Gen #{gen} (4 spiders): {ru_q}\n" + code_txt + "\n")
        r_test = subprocess.run(["python3", mod_name], capture_output=True, text=True, timeout=6)
        if r_test.returncode == 0 and r_test.stdout.strip():
            mod_status = f"Модуль {os.path.basename(mod_name)} ({len(intel_list)} источу.) -> {r_test.stdout.strip()[:85]}"
        else:
            os.remove(mod_name)

clean_note = re.sub(r"```python.*?```", "", synthesis, flags=re.S).strip()[:420] or combined_intel[:420]
rec = f"[Рой-Эволюция Gen #{gen} | {now_s}] Тема: {ru_q} | Источников: {len(intel_list)} | {clean_note} | {mod_status}"

# 4. Упаковка в сжатый мозг zlib-9 и сохранение в облако
with open("chat_knowledge.txt", "a", encoding="utf-8") as f:
    f.write(rec + "\n")
raw_b = zlib.decompress(open(BRAIN_ZLIB, "rb").read()) if os.path.exists(BRAIN_ZLIB) else b""
open(BRAIN_ZLIB, "wb").write(zlib.compress(raw_b + (rec + "\n").encode("utf-8"), level=9))

feed = json.loads(open("cloud_feed.json", encoding="utf-8").read()) if os.path.exists("cloud_feed.json") else []
feed.append({"src": f"4-Паука Gen #{gen}", "title": f"{ru_q} ({len(intel_list)} науч. сайта)", "info": clean_note, "time": now_s})
open("cloud_feed.json", "w", encoding="utf-8").write(json.dumps(feed[-60:], ensure_ascii=False, indent=2))

evo["gen"] = gen
evo["history"].append({"gen": gen, "topic": ru_q, "sources": len(intel_list), "status": mod_status, "time": now_s})
open(EVO_LOG, "w", encoding="utf-8").write(json.dumps(evo[-50:], ensure_ascii=False, indent=2))
print(f"4-Spider Evolution Gen #{gen} complete: {ru_q} ({len(intel_list)} sources)")
