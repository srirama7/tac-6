#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv"]
# ///
import subprocess
import os
import sys
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Print environment variables
print("ANTHROPIC_API_KEY:", os.getenv("ANTHROPIC_API_KEY"))
print("CLAUDE_CODE_PATH:", os.getenv("CLAUDE_CODE_PATH"))

# Try running Claude Code
cmd = [
    os.getenv("CLAUDE_CODE_PATH", "claude"),
    "-p",
    "/classify_issue {\"number\":21,\"title\":\"Test\",\"body\":\"Test\"}",
    "--model",
    "sonnet",
    "--output-format",
    "stream-json",
    "--verbose"
]

print("\nRunning command:", " ".join(cmd))
print("\nEnvironment passed to Claude:")

# Build environment like agent.py does
env = {
    "CLAUDE_CODE_PATH": os.getenv("CLAUDE_CODE_PATH", "claude"),
    "HOME": os.getenv("HOME"),
    "USER": os.getenv("USER"),
    "PATH": os.getenv("PATH"),
    "SHELL": os.getenv("SHELL"),
    "TERM": os.getenv("TERM"),
}
# Filter None values
env = {k: v for k, v in env.items() if v is not None}

for k, v in env.items():
    if "KEY" not in k and "TOKEN" not in k:
        print(f"  {k}: {v[:50] if len(str(v)) > 50 else v}")
    else:
        print(f"  {k}: (hidden)")

print("\nRunning Claude Code...")
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env, cwd="C:/Users/amogh/Downloads/tac5new/tac-5")

print("\nReturn code:", result.returncode)
print("Stdout:", result.stdout[:500] if result.stdout else "(empty)")
print("Stderr:", result.stderr[:500] if result.stderr else "(empty)")
