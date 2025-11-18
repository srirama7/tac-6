"""Claude Code agent module for executing prompts programmatically."""

import subprocess
import sys
import os
import json
import re
from typing import Optional, List, Dict, Any, Tuple
from dotenv import load_dotenv
from .data_types import (
    AgentPromptRequest,
    AgentPromptResponse,
    AgentTemplateRequest,
    ClaudeCodeResultMessage,
)

# Load environment variables
load_dotenv()

# Get Claude Code CLI path from environment
CLAUDE_PATH = os.getenv("CLAUDE_CODE_PATH", "claude")


def check_claude_installed() -> Optional[str]:
    """Check if Claude Code CLI is installed. Return error message if not."""
    try:
        result = subprocess.run(
            [CLAUDE_PATH, "--version"], capture_output=True, text=True
        )
        if result.returncode != 0:
            return (
                f"Error: Claude Code CLI is not installed. Expected at: {CLAUDE_PATH}"
            )
    except FileNotFoundError:
        return f"Error: Claude Code CLI is not installed. Expected at: {CLAUDE_PATH}"
    return None


def parse_jsonl_output(
    output_file: str,
) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Parse JSONL output file and return all messages and the result message.

    Returns:
        Tuple of (all_messages, result_message) where result_message is None if not found
    """
    try:
        # First try UTF-8, then fall back to reading raw bytes if that fails
        try:
            with open(output_file, "r", encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            # If UTF-8 fails, read as binary and decode with replace
            with open(output_file, "rb") as f:
                content = f.read().decode('utf-8', errors='replace')

        # Parse each line as JSON
        messages = []
        for line in content.split('\n'):
            line = line.strip()
            if line:
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: Failed to parse JSON line: {e}", file=sys.stderr)
                    continue

        # Find the result message (should be the last one)
        result_message = None
        for message in reversed(messages):
            if message.get("type") == "result":
                result_message = message
                break

        return messages, result_message
    except Exception as e:
        print(f"Error parsing JSONL file: {e}", file=sys.stderr)
        return [], None


def convert_jsonl_to_json(jsonl_file: str) -> str:
    """Convert JSONL file to JSON array file.

    Creates a .json file with the same name as the .jsonl file,
    containing all messages as a JSON array.

    Returns:
        Path to the created JSON file
    """
    # Create JSON filename by replacing .jsonl with .json
    json_file = jsonl_file.replace(".jsonl", ".json")

    # Parse the JSONL file
    messages, _ = parse_jsonl_output(jsonl_file)

    # Write as JSON array
    with open(json_file, "w", encoding='utf-8') as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(f"Created JSON file: {json_file}")
    return json_file


def get_claude_env() -> Dict[str, str]:
    """Get environment variables for Claude Code execution.

    Returns a dictionary containing the full system environment
    with specific overrides for Claude Code configuration.

    On Windows, many system environment variables (SystemRoot, WINDIR, etc.)
    are required for executables to run properly, so we inherit the full
    environment and only override specific values.
    """
    # Start with the full system environment
    env = os.environ.copy()

    # Override/add specific values if they exist
    if os.getenv("ANTHROPIC_API_KEY"):
        env["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

    if os.getenv("CLAUDE_CODE_PATH"):
        env["CLAUDE_CODE_PATH"] = os.getenv("CLAUDE_CODE_PATH")

    if os.getenv("CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR"):
        env["CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR"] = os.getenv(
            "CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR", "true"
        )

    if os.getenv("E2B_API_KEY"):
        env["E2B_API_KEY"] = os.getenv("E2B_API_KEY")

    # Add GitHub tokens if GITHUB_PAT exists
    github_pat = os.getenv("GITHUB_PAT")
    if github_pat:
        env["GITHUB_PAT"] = github_pat
        env["GH_TOKEN"] = github_pat  # Claude Code uses GH_TOKEN

    return env


def save_prompt(prompt: str, adw_id: str, agent_name: str = "ops") -> str:
    """Save a prompt to the appropriate logging directory.

    Returns:
        Path to the saved prompt file
    """
    # Extract slash command from prompt
    match = re.match(r"^(/\w+)", prompt)
    if not match:
        # If no slash command found, use a generic name
        command_name = "prompt"
    else:
        slash_command = match.group(1)
        # Remove leading slash for filename
        command_name = slash_command[1:]

    # Create directory structure at project root (parent of adws)
    # __file__ is in adws/adw_modules/, so we need to go up 3 levels to get to project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    prompt_dir = os.path.join(project_root, "agents", adw_id, agent_name, "prompts")
    os.makedirs(prompt_dir, exist_ok=True)

    # Save prompt to file
    prompt_file = os.path.join(prompt_dir, f"{command_name}.txt")
    with open(prompt_file, "w", encoding='utf-8') as f:
        f.write(prompt)

    print(f"Saved prompt to: {prompt_file}")
    return prompt_file


def prompt_claude_code(request: AgentPromptRequest) -> AgentPromptResponse:
    """Execute Claude Code with the given prompt configuration."""

    # Check if Claude Code CLI is installed
    error_msg = check_claude_installed()
    if error_msg:
        return AgentPromptResponse(output=error_msg, success=False, session_id=None)

    # Save prompt before execution
    prompt_file = save_prompt(request.prompt, request.adw_id, request.agent_name)

    # Create output directory if needed
    output_dir = os.path.dirname(request.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Build command - use stdin to pass prompt (avoids Windows command-line length limits)
    cmd = [CLAUDE_PATH]
    cmd.extend(["--model", request.model])
    cmd.extend(["-p"])  # Enable print mode
    cmd.extend(["--verbose"])
    cmd.extend(["--output-format", "stream-json"])

    # Add dangerous skip permissions flag if enabled
    if request.dangerously_skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    # Set up environment with only required variables
    env = get_claude_env()

    try:
        # Debug: print the command being executed
        print(f"DEBUG: Executing command: {' '.join(cmd)}")
        print(f"DEBUG: Working directory: {os.getcwd()}")
        print(f"DEBUG: Output file: {request.output_file}")
        print(f"DEBUG: Prompt length: {len(request.prompt)} characters")

        # Execute Claude Code with prompt via stdin and pipe output to file
        with open(request.output_file, "w", encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                input=request.prompt,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )

        print(f"DEBUG: Return code: {result.returncode}")
        print(f"DEBUG: Stderr: {result.stderr[:500] if result.stderr else '(empty)'}")

        if result.returncode == 0:
            print(f"Output saved to: {request.output_file}")

            # Parse the JSONL file
            messages, result_message = parse_jsonl_output(request.output_file)

            # Convert JSONL to JSON array file
            json_file = convert_jsonl_to_json(request.output_file)

            if result_message:
                # Extract session_id from result message
                session_id = result_message.get("session_id")

                # Check if there was an error in the result
                is_error = result_message.get("is_error", False)
                subtype = result_message.get("subtype", "")
                
                # Handle error_during_execution case where there's no result field
                if subtype == "error_during_execution":
                    error_msg = "Error during execution: Agent encountered an error and did not return a result"
                    return AgentPromptResponse(
                        output=error_msg, success=False, session_id=session_id
                    )
                
                result_text = result_message.get("result", "")

                return AgentPromptResponse(
                    output=result_text, success=not is_error, session_id=session_id
                )
            else:
                # No result message found, return raw output
                with open(request.output_file, "r") as f:
                    raw_output = f.read()
                return AgentPromptResponse(
                    output=raw_output, success=True, session_id=None
                )
        else:
            # Check for fatal Windows error codes that indicate crashes
            # 3221226505 (0xC0000409) = STATUS_STACK_BUFFER_OVERRUN
            fatal_error_codes = [3221226505, 3221225477]  # Common crash codes

            if result.returncode in fatal_error_codes:
                error_msg = f"Claude Code CLI crashed with fatal error (code: {result.returncode}). This is a critical error that cannot be automatically resolved."
            elif result.stderr:
                error_msg = f"Claude Code error: {result.stderr}"
            else:
                error_msg = f"Claude Code failed with exit code {result.returncode} (no error message available)"

            print(error_msg, file=sys.stderr)
            return AgentPromptResponse(output=error_msg, success=False, session_id=None)

    except subprocess.TimeoutExpired:
        error_msg = "Error: Claude Code command timed out after 5 minutes"
        print(error_msg, file=sys.stderr)
        return AgentPromptResponse(output=error_msg, success=False, session_id=None)
    except Exception as e:
        error_msg = f"Error executing Claude Code: {e}"
        print(error_msg, file=sys.stderr)
        return AgentPromptResponse(output=error_msg, success=False, session_id=None)


def execute_template(request: AgentTemplateRequest) -> AgentPromptResponse:
    """Execute a Claude Code template with slash command and arguments."""
    # Check if slash_command is a custom command that needs to be loaded from file
    if request.slash_command.startswith("/"):
        # Get project root and check for slash command file
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        command_name = request.slash_command[1:]  # Remove leading slash
        command_file = os.path.join(project_root, ".claude", "commands", f"{command_name}.md")

        if os.path.exists(command_file):
            # Read the command file content and use it as the prompt
            with open(command_file, "r", encoding='utf-8') as f:
                prompt = f.read()
            # Append args if any
            if request.args:
                prompt += "\n\n" + " ".join(request.args)
        else:
            # Slash command file doesn't exist, use as-is (might be a built-in command)
            prompt = f"{request.slash_command} {' '.join(request.args)}"
    else:
        # Not a slash command, use as-is
        prompt = f"{request.slash_command} {' '.join(request.args)}"

    # Create output directory with adw_id at project root
    # __file__ is in adws/adw_modules/, so we need to go up 3 levels to get to project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(
        project_root, "agents", request.adw_id, request.agent_name
    )
    os.makedirs(output_dir, exist_ok=True)

    # Build output file path
    output_file = os.path.join(output_dir, "raw_output.jsonl")

    # Create prompt request with specific parameters
    prompt_request = AgentPromptRequest(
        prompt=prompt,
        adw_id=request.adw_id,
        agent_name=request.agent_name,
        model=request.model,
        dangerously_skip_permissions=True,
        output_file=output_file,
    )

    # Execute and return response (prompt_claude_code now handles all parsing)
    return prompt_claude_code(prompt_request)
