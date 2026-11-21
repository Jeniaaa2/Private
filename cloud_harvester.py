import os, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime

MEM = "chat_knowledge.txt"
if not os.path.exists(MEM):
    open(MEM, "w", encoding="utf-8").write("Облачная база знаний ИИ.\n")

entries = []
try:
    u = "http://arxiv.org"
    root = ET.fromstring(urllib.request.urlopen(u, timeout=15).read())
    ns = {"a": "http://w3.org"}
    for e in root.findall("a:entry", ns):
        t = e.find("a:title", ns).text.strip().replace("\n", " ")
        entries.append(f"[Cloud-arXiv {datetime.utcnow().strftime('%H:%M')}] {t}")
except Exception:
    pass

if entries:
    existing = open(MEM, encoding="utf-8").read()
    with open(MEM, "a", encoding="utf-8") as f:
        for line in entries:
            if line not in existing:
                f.write(line + "\n")
                print("Добавлено:", line)
