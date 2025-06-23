from flask import Flask, request, jsonify
import os
from utils import execute_generated_code
import requests

app = Flask(__name__)

TASKS_DIR = "tasks"
MAX_RETRIES = 3

os.makedirs(TASKS_DIR, exist_ok=True)

def call_ollama(prompt, model="llama3"):
    try:
        print(f"📦 [Ollama] Sending prompt to local model '{model}'...")
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        res.raise_for_status()
        return res.json().get("response", "")
    except Exception as e:
        return f"[Ollama Error] {str(e)}"

def generate_code_with_auto_fix(original_prompt, task_dir):
    prompt = original_prompt
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"🤖 Attempt #{attempt} generating code...")
        code = call_ollama(prompt)
        filepath = os.path.join(task_dir, "generated_code.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        execution_result = execute_generated_code(filepath)
        log_path = os.path.join(task_dir, "execution_log.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(execution_result)

        # Check if error happened
        if "Traceback" not in execution_result and "Error" not in execution_result:
            print("✅ Code executed without errors!")
            return code, execution_result
        else:
            print("⚠️ Error detected, preparing fix prompt...")
            error_summary = execution_result.replace("\n", " ")
            # Append fix instruction to prompt
            prompt = (
                original_prompt + 
                f"\n\n# The following error occurred when running the previous code:\n# {error_summary}\n"
                "# Please fix the code and only return the corrected full script."
            )

    print("❌ Max retries reached, returning last code and errors.")
    return code, execution_result

@app.route("/generate_code", methods=["POST"])
def generate_code_endpoint():
    data = request.json
    prompt = data.get("prompt")
    task_id = data.get("task_id")

    if not prompt or not task_id:
        return jsonify({"error": "Missing 'prompt' or 'task_id'"}), 400

    task_dir = os.path.join(TASKS_DIR, task_id)
    os.makedirs(task_dir, exist_ok=True)

    generated_code, execution_log = generate_code_with_auto_fix(prompt, task_dir)

    return jsonify({
        "task_id": task_id,
        "generated_code": generated_code,
        "execution_log": execution_log
    })

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
