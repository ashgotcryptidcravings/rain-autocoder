import requests

def call_ollama(prompt, model="llama3"):
    try:
        print(f"📦 [Ollama] Sending prompt to local model '{model}'...")
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        res.raise_for_status()
        return res.json()["response"]
    except Exception as e:
        return f"[Ollama Error] {str(e)}"

def generate_code(prompt, prefer_local=True):
    print("🧠 Generating code with local model (LLaMA3)...")
    return call_ollama(prompt, model="llama3")
