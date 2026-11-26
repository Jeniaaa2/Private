
def fetch_pubmed(query):
    try:
        import urllib.request as ur, urllib.parse as up, json as js
        q = up.quote(query)
        u_s = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={q}&retmode=json&retmax=2"
        ids = js.loads(ur.urlopen(u_s, timeout=10).read().decode()).get("esearchresult", {}).get("idlist", [])
        if not ids:
            return ""
        u_sum = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=json"
        res = js.loads(ur.urlopen(u_sum, timeout=10).read().decode()).get("result", {})
        titles = [res[i].get("title", "") for i in ids if i in res]
        return "[PubMed] " + " | ".join(t for t in titles if t) if titles else ""
    except Exception:
        return ""

import subprocess
print("=== ЗАПУСК ОБЛАЧНЫХ ИИ-АГЕНТОВ НА СЕРВЕРЕ GITHUB ===")
subprocess.run(["python3", "cloud_agents.py"], check=False)
