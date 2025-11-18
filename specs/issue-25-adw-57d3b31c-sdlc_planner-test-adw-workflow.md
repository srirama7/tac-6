# Chore: Test ADW Workflow

## Chore Description
This is a test issue created to validate the AI Developer Workflow (ADW) system. The workflow includes planning, building, and testing phases that are orchestrated through automated agents. This test ensures that all components of the ADW system work correctly together.

## Relevant Files
Use these files to resolve the chore:

- `adws/adw_plan_build_test.py` - Main orchestrator script that chains together the plan, build, and test phases
- `adws/adw_plan.py` - Planning phase script that classifies issues, generates branches, and creates implementation plans
- `adws/adw_build.py` - Build phase script that implements the plan
- `adws/adw_test.py` - Test phase script that validates the implementation
- `adws/adw_modules/workflow_ops.py` - Core workflow operations including issue classification, branch generation, and plan building
- `adws/adw_modules/agent.py` - Claude Code agent module for executing prompts programmatically
- `adws/adw_modules/state.py` - ADW state management
- `.claude/commands/chore.md` - Chore planning slash command template
- `.claude/commands/find_plan_file.md` - Plan file finder slash command template

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Verify ADW State Management
- Ensure adw_state.json is being created and persisted correctly across workflow phases
- Verify state includes: adw_id, issue_number, branch_name, plan_file, issue_class
- Confirm state is properly loaded and updated by each workflow script

### 2. Validate Issue Classification
- Test that issues are correctly classified as /chore, /bug, or /feature
- Ensure classification agent returns valid slash command format
- Verify error handling for invalid classifications

### 3. Test Branch Generation
- Confirm branch names follow the pattern: {issue_class}-issue-{number}-adw-{adw_id}-{description}
- Verify branch generation agent extracts clean branch names from responses
- Test branch creation and switching

### 4. Verify Plan File Creation
- Ensure sdlc_planner agent creates plan files in specs/ directory
- Confirm plan file naming: issue-{number}-adw-{adw_id}-sdlc_planner-{description}.md
- Validate plan_finder agent can locate the created plan file
- Test plan file format matches the required template

### 5. Test Build Phase Integration
- Verify adw_build.py can load the plan file from state
- Confirm implementor agent executes the plan steps
- Test error handling during implementation

### 6. Test Testing Phase Integration
- Verify adw_test.py runs appropriate validation commands
- Confirm test results are properly reported
- Test handling of test failures

### 7. Validate End-to-End Workflow
- Run complete workflow from issue number input to test completion
- Verify all state transitions are correct
- Confirm GitHub comments are posted at each phase
- Test PR creation and updates

### 8. Run Validation Commands
Execute every validation command to ensure zero regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `uv run adws/adw_plan_build_test.py 25 57d3b31c` - Run the complete workflow to ensure it executes without errors
- `cd app/server && uv run pytest` - Run server tests to validate no regressions

## Notes
- The workflow uses persistent state stored in `agents/{adw_id}/adw_state.json`
- All agent outputs are logged to `agents/{adw_id}/{agent_name}/` directories
- The system uses Claude Code CLI for executing prompts programmatically
- Slash commands are defined in `.claude/commands/` and expanded by Claude Code
- GitHub integration requires GITHUB_PAT environment variable
