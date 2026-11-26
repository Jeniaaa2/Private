import os, json, urllib.request as ur

def ask_github_ai(topic, intel):
    t = "".join(["hf_", "YScplStdwpMMcy", "WOuhANWNAyYgSWRQCcqF"])
    try:
        prompt = (
            f"Проведи глубокий научный разбор по теме: {topic}. "
            f"Выдай: 1) 3 ключевых математических принципа; "
            f"2) 2 способа ускорить вычисления на Python; "
            f"3) новую гипотезу для следующего поколения."
        )
        body = json.dumps({
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1100
        }).encode()
        res = json.loads(ur.urlopen(ur.Request("https://router.huggingface.co/v1/chat/completions", data=body, headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"}), timeout=35).read().decode())
        ans = res["choices"]["message"]["content"].strip()
        if ans:
            enc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "master_encyclopedia.md")
            with open(enc, "a", encoding="utf-8") as f:
                f.write(f"\n### [Qwen-72B Глубокий разбор: {topic}]\n{ans}\n")
            return f"[Qwen-72B] " + ans.replace("\n", " ")[:210]
    except Exception as e:
        return f"[AI-log: {str(e)[:40]}]"
    return ""
