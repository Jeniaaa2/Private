import os, json, urllib.request as ur

def ask_github_ai(topic, intel):
    tok = os.environ.get("GITHUB_TOKEN", "").strip()
    if not tok:
        return ""
    try:
        url = "https://models.inference.ai.azure.com/chat/completions"
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": f"Дай 2 кратких научных вывода и 1 идею оптимизации по теме: {topic}. Факты: {intel[:500]}"}],
            "max_tokens": 160
        }).encode("utf-8")
        req = ur.Request(url, data=payload, headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
        resp = json.loads(ur.urlopen(req, timeout=20).read().decode("utf-8"))
        ans = resp["choices"][0]["message"]["content"].strip().replace("\n", " ")
        return f"[GitHub-AI] {ans[:260]}" if ans else ""
    except Exception:
        return ""
