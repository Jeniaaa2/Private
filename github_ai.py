import os, json, urllib.request as ur

def ask_github_ai(topic, intel):
    tok = os.environ.get("GITHUB_TOKEN", "").strip()
    if not tok:
        return ""
    try:
        prompt = (
            f"Проведи глубокий научный разбор по теме: {topic}. "
            f"Контекст: {intel[:800]}. "
            f"Выдай: 1) 3 ключевых математических принципа; "
            f"2) 2 конкретных способа ускорить вычисления на Python; "
            f"3) новую гипотезу для следующего поколения эволюции."
        )
        body = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1200
        }).encode()
        res = json.loads(ur.urlopen(ur.Request("https://models.inference.ai.azure.com/chat/completions", data=body, headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}), timeout=35).read().decode())
        ans = res["choices"]["message"]["content"].strip()
        if ans:
            enc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "master_encyclopedia.md")
            with open(enc, "a", encoding="utf-8") as f:
                f.write(f"\n### [GitHub-AI Глубокий разбор: {topic}]\n{ans}\n")
            short = ans.replace("\n", " ")[:220]
            return f"[GitHub-AI 1200t] {short}"
    except Exception:
        pass
    return ""
