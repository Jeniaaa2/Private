import os, json, hashlib, time

CLD = os.path.expanduser("~/ai_cloud")
HASH_DB = os.path.join(CLD, "seen_hashes.json")
ENCYCLOPEDIA = os.path.join(CLD, "master_encyclopedia.md")

def filter_and_catalog(gen_num, topic, raw_text):
    seen = set()
    if os.path.exists(HASH_DB):
        try:
            seen = set(json.loads(open(HASH_DB, encoding="utf-8").read()))
        except Exception:
            pass

    chunks = [c.strip() for c in raw_text.split("||") if len(c.strip()) > 35]
    novel_chunks = []
    for ch in chunks:
        norm = " ".join(ch.lower().split())
        sig = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]
        if sig not in seen:
            seen.add(sig)
            novel_chunks.append(ch)

    open(HASH_DB, "w", encoding="utf-8").write(json.dumps(sorted(list(seen))[-1500:]))

    if novel_chunks:
        ts = time.strftime("%Y-%m-%d %H:%M UTC")
        header_needed = not os.path.exists(ENCYCLOPEDIA)
        with open(ENCYCLOPEDIA, "a", encoding="utf-8") as f:
            if header_needed:
                f.write("# 🧠 Сводная научная энциклопедия облачного ИИ (без дублей)\n\n")
            f.write(f"## Gen #{gen_num} — {topic} ({ts})\n")
            for item in novel_chunks:
                f.write(f"- {item[:320]}\n")
            f.write("\n")
    return len(novel_chunks), len(chunks)
