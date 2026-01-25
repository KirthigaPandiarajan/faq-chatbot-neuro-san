# backend/app/agent_logic.py
import subprocess
import json

def get_bot_response(user_message: str) -> str:
    process = subprocess.Popen(
        [
            "python",
            "-m",
            "neuro_san.client.agent_cli",
            "--agent",
            "faq_agent"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(user_message + "\n")

    if process.returncode != 0:
        raise RuntimeError(stderr)

    return stdout.strip()
