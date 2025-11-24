"""Test Claude Code subprocess execution to debug slash command loading."""
import subprocess
import sys
import os

# Get project root (current directory)
project_root = os.getcwd()
print(f"Project root: {project_root}")
print(f".claude directory exists: {os.path.exists(os.path.join(project_root, '.claude'))}")
print(f".claude/commands directory exists: {os.path.exists(os.path.join(project_root, '.claude', 'commands'))}")

# List command files
commands_dir = os.path.join(project_root, '.claude', 'commands')
if os.path.exists(commands_dir):
    commands = os.listdir(commands_dir)
    print(f"Command files: {commands[:5]}...")  # Show first 5

# Build command
cmd = ["claude", "--print", "--model", "sonnet", "--output-format", "stream-json", "--verbose", "--dangerously-skip-permissions"]

# Set up environment
env = os.environ.copy()
if sys.platform == 'win32':
    env["CLAUDE_DISABLE_HOOKS"] = "true"

# Test prompt
prompt = '/classify_issue {"number": 31, "title": "test", "body": "add export feature"}'
print(f"\nPrompt: {prompt}")
print(f"CWD: {project_root}")
print(f"Command: {' '.join(cmd)}")

# Execute
print("\nExecuting...")
process = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='utf-8',
    errors='replace',
    env=env,
    cwd=project_root
)

stdout_data, stderr_data = process.communicate(input=prompt)

print(f"\nReturn code: {process.returncode}")
if stderr_data:
    print(f"Stderr: {stderr_data}")

# Parse first line to see slash commands
import json
if stdout_data:
    lines = stdout_data.strip().split('\n')
    if lines:
        try:
            init_msg = json.loads(lines[0])
            if init_msg.get('type') == 'system' and init_msg.get('subtype') == 'init':
                slash_commands = init_msg.get('slash_commands', [])
                print(f"\nSlash commands loaded: {len(slash_commands)}")
                print(f"classify_issue in list: {'classify_issue' in slash_commands}")
                if 'classify_issue' not in slash_commands:
                    print(f"Commands: {slash_commands}")
        except:
            pass

    # Look for result
    for line in lines:
        try:
            msg = json.loads(line)
            if msg.get('type') == 'result':
                result = msg.get('result', '')
                print(f"\nResult: '{result}'")
                print(f"Success: {not msg.get('is_error', False)}")
                usage = msg.get('usage', {})
                print(f"Input tokens: {usage.get('input_tokens', 0)}")
                print(f"Output tokens: {usage.get('output_tokens', 0)}")
        except:
            pass
