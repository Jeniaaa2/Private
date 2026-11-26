import os, re, json, zlib, lzma, urllib.request as ur, urllib.parse as up

BASE = os.path.dirname(os.path.abspath(__file__))
ULTRA_BRAIN = os.path.join(BASE, "ultra_brain.xz")

def fetch_extra_sources(topic):
    out = []
    q = up.quote(topic[:80])
    # 1. Semantic Scholar Open API (свежие научные аннотации по ИИ и алгоритмам)
    try:
        u1 = f"https://semanticscholar.org{q}&limit=2&fields=title,abstract"
        req1 = ur.Request(u1, headers={"User-Agent": "CloudResearchBot/1.0"})
        d1 = json.loads(ur.urlopen(req1, timeout=10).read().decode("utf-8"))
        for p in d1.get("data", []):
            ab = (p.get("abstract") or "").strip()
            if ab:
                out.append(f"[SemanticScholar] {p.get('title','')}: {ab[:260]}")
    except Exception:
        pass
    # 2. Crossref Open API (рецензируемые публикации)
    try:
        u2 = f"https://crossref.org{q}&rows=2&select=title,subject"
        req2 = ur.Request(u2, headers={"User-Agent": "CloudResearchBot/1.0"})
        d2 = json.loads(ur.urlopen(req2, timeout=10).read().decode("utf-8"))
        for it in d2.get("message", {}).get("items", []):
            tl = next(iter(it.get("title", [])), "")
            if tl:
                out.append(f"[Crossref] {tl[:180]}")
    except Exception:
        pass
    return " || ".join(out)

def distill_and_compress(raw_text):
    # Семантическая дистилляция: убираем воду и дубли, оставляем плотные факты
    sents = re.split(r"(?<=[.!?])\s+|\|\|", raw_text)
    seen, core = set(), []
    for s in sents:
        cl = re.sub(r"\s+", " ", s).strip()
        if len(cl) < 28:
            continue
        key = cl[:48].lower()
        if key not in seen:
            seen.add(key)
            core.append(cl)
    distilled = " | ".join(core).encode("utf-8")
    if not distilled:
        return "Сжатие: 1.0x"

    prev = b""
    if os.path.exists(ULTRA_BRAIN):
        try:
            prev = lzma.decompress(open(ULTRA_BRAIN, "rb").read())
        except Exception:
            prev = b""
    merged = (prev + b"\n" + distilled)[-180000:]
    packed = lzma.compress(merged, preset=9)
    open(ULTRA_BRAIN, "wb").write(packed)
    ratio = round(len(merged) / max(1, len(packed)), 2)
    return f"Сжатие LZMA: {ratio}x ({len(merged)}->{len(packed)} Б)"
