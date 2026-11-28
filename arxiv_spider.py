import urllib.request, urllib.parse, xml.etree.ElementTree as ET, os

BASE = os.path.dirname(os.path.abspath(__file__))

def fetch_arxiv(topic="quantum graph compression"):
    try:
        q = urllib.parse.quote(topic)
        host = "export." + "arxiv.org"
        url = f"https://{host}/api/query?search_query=all:{q}&start=0&max_results=2"
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchBot/1.0"})
        xml_data = urllib.request.urlopen(req, timeout=10).read()
        root = ET.fromstring(xml_data)
        titles = []
        for el in root.iter():
            if el.tag.endswith("entry"):
                t, s = "", ""
                for ch in el:
                    if ch.tag.endswith("title"): t = " ".join((ch.text or "").split())
                    if ch.tag.endswith("summary"): s = " ".join((ch.text or "").split())[:200]
                if t: titles.append(f"{t} ({s}...)")
        if titles:
            with open(os.path.join(BASE, "master_encyclopedia.md"), "a", encoding="utf-8") as f:
                f.write(f"\n### [arXiv Внешний поиск: {topic}]\n" + "\n".join(f"- {x}" for x in titles) + "\n")
            return f" | 🔭 arXiv: найдено {len(titles)} науч. работ"
    except Exception as e:
        return f" | 🔭 arXiv err: {str(e)[:30]}"
    return ""
