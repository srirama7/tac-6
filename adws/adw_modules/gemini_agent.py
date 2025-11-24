"""Gemini API agent module for executing prompts without Claude Code CLI."""

import os
import json
import re
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai
from .data_types import (
    AgentPromptRequest,
    AgentPromptResponse,
    AgentTemplateRequest,
)

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def save_prompt(prompt: str, adw_id: str, agent_name: str = "ops") -> None:
    """Save a prompt to the appropriate logging directory."""
    # Extract slash command from prompt
    match = re.match(r"^(/\w+)", prompt)
    if not match:
        return

    slash_command = match.group(1)
    # Remove leading slash for filename
    command_name = slash_command[1:]

    # Create directory structure at project root (parent of adws)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    prompt_dir = os.path.join(project_root, "agents", adw_id, agent_name, "prompts")
    os.makedirs(prompt_dir, exist_ok=True)

    # Save prompt to file
    prompt_file = os.path.join(prompt_dir, f"{command_name}.txt")
    with open(prompt_file, "w", encoding='utf-8') as f:
        f.write(prompt)

    print(f"Saved prompt to: {prompt_file}")


def prompt_gemini(request: AgentPromptRequest) -> AgentPromptResponse:
    """Execute Gemini API with the given prompt configuration."""

    if not GEMINI_API_KEY:
        return AgentPromptResponse(
            output="Error: GEMINI_API_KEY not set in environment",
            success=False,
            session_id=None
        )

    # Save prompt before execution
    save_prompt(request.prompt, request.adw_id, request.agent_name)

    # Create output directory if needed
    output_dir = os.path.dirname(request.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        # Map model names
        model_map = {
            "sonnet": "gemini-2.0-flash-exp",  # Use Gemini 2.0 Flash for fast responses
            "opus": "gemini-2.0-flash-thinking-exp",  # Use thinking model for complex tasks
            "haiku": "gemini-2.0-flash-exp"  # Use Flash for lightweight tasks
        }
        gemini_model_name = model_map.get(request.model, "gemini-2.0-flash-exp")

        # Create Gemini model
        model = genai.GenerativeModel(gemini_model_name)

        # Generate response
        response = model.generate_content(request.prompt)

        # Extract text from response
        if response.text:
            result_text = response.text

            # Save to output file
            output_data = {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "result": result_text,
                "session_id": request.adw_id,
                "model": gemini_model_name
            }

            with open(request.output_file, "w", encoding='utf-8') as f:
                f.write(json.dumps(output_data) + "\n")

            print(f"Output saved to: {request.output_file}")

            return AgentPromptResponse(
                output=result_text,
                success=True,
                session_id=request.adw_id
            )
        else:
            error_msg = "Gemini returned empty response"
            return AgentPromptResponse(
                output=error_msg,
                success=False,
                session_id=None
            )

    except Exception as e:
        error_msg = f"Error executing Gemini API: {str(e)}"
        print(error_msg)
        return AgentPromptResponse(
            output=error_msg,
            success=False,
            session_id=None
        )


def execute_template(request: AgentTemplateRequest) -> AgentPromptResponse:
    """Execute a template with slash command and arguments using Gemini."""
    # Construct prompt from slash command and args
    prompt = f"{request.slash_command} {' '.join(request.args)}"

    # Create output directory with adw_id at project root
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

    # Execute and return response
    return prompt_gemini(prompt_request)
