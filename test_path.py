import os

# Simulate agent.py path calculation
file_path = r"C:\Users\amogh\Downloads\tac-6\tac-6\adws\adw_modules\agent.py"
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(file_path))))
print(f"Calculated project root: {project_root}")
print(f".claude exists: {os.path.exists(os.path.join(project_root, '.claude'))}")
print(f".claude/commands exists: {os.path.exists(os.path.join(project_root, '.claude', 'commands'))}")

# List some commands
commands_dir = os.path.join(project_root, '.claude', 'commands')
if os.path.exists(commands_dir):
    commands = [f for f in os.listdir(commands_dir) if f.endswith('.md')]
    print(f"Found {len(commands)} command files")
    print(f"classify_issue.md exists: {'classify_issue.md' in commands}")
