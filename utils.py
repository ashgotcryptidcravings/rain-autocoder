import subprocess
import os

def execute_generated_code(file_path):
    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "[Execution Error] Code timed out after 10 seconds."
    except Exception as e:
        return f"[Execution Error] {str(e)}"
