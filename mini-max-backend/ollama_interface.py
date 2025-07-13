import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_ollama(prompt: str) -> str:
    system_prompt = (
        "You are Derick, an expert coding assistant.\n"
        "ONLY respond with valid, clean code. Do not explain.\n"
        "Do not wrap code in backticks or markdown.\n"
    )
    full_prompt = f"{system_prompt}\nUser Prompt:\n{prompt}\n\nAnswer:\n"

    payload = {
        "model": "derick",  # your Ollama model name
        "prompt": full_prompt,
        "stream": False,
        "temperature": 0.7
    }

    try:
        res = requests.post(OLLAMA_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        if res.status_code == 200:
            return res.json().get("response", "").strip()
        else:
            print("❌ Ollama error:", res.status_code, res.text)
            return "Error from Derick backend."
    except Exception as e:
        print("❌ Exception in contacting Ollama:", str(e))
        return "Error contacting Ollama."
