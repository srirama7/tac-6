# Chore: Test Issue #25

## Chore Description
This is a test issue created to validate the ADW (AI Developer Workflow) automation system. The chore involves verifying that the complete ADW workflow functions correctly from issue classification through plan generation, implementation, testing, and pull request creation. This test ensures the workflow can properly process GitHub issues, classify them, generate implementation plans, and create structured documentation in the specs directory.

The test validates:
- Issue classification using the `/chore` command
- Branch creation with proper naming convention (`{type}-issue-{number}-adw-{id}-{slug}`)
- Plan generation using Claude Code CLI integration
- Spec file creation in the `specs/` directory
- Git operations (commits, pull requests)
- State management across workflow phases
- Comment posting to GitHub issues for tracking

## Relevant Files
Use these files to resolve the chore:

- `adws/adw_plan.py` - Main planning phase script that orchestrates the workflow
  - Handles issue fetching, classification, branch creation, and plan generation
  - Entry point for the planning phase of ADW

- `adws/adw_modules/workflow_ops.py` - Core workflow operations
  - Contains `classify_issue()` for issue classification
  - Contains `build_plan()` for plan generation
  - Contains `generate_branch_name()` for branch naming
  - Business logic extracted for reusability

- `adws/adw_modules/agent.py` - Claude Code CLI integration
  - Executes Claude Code commands via subprocess
  - Manages agent templates and prompt execution
  - Handles JSONL output parsing

- `adws/adw_modules/state.py` - State management for workflow chaining
  - `ADWState` class for persisting workflow state
  - Enables chaining workflows via JSON piping
  - Stores adw_id, issue_number, branch_name, plan_file, issue_class

- `adws/adw_modules/git_ops.py` - Git operations
  - Branch creation, commits, and pull request management
  - Handles `create_branch()`, `commit_changes()`, `finalize_git_operations()`

- `adws/adw_modules/github.py` - GitHub API operations
  - Issue fetching via `gh` CLI
  - Comment posting for tracking
  - Repository URL extraction

- `README.md` - Project documentation
  - Contains ADW system overview and usage instructions
  - Documents environment variables and prerequisites

### New Files
- `specs/issue-25-adw-2c3c1641-sdlc_planner-test-adw-workflow.md` - This plan file (self-documenting)

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Verify ADW Environment Setup
- Confirm that all required environment variables are set:
  - `GITHUB_REPO_URL` - Repository URL for GitHub operations
  - `ANTHROPIC_API_KEY` - API key for Claude Code CLI
  - `CLAUDE_CODE_PATH` - Path to Claude Code executable (defaults to "claude")
- Verify that GitHub CLI (`gh`) is authenticated and working
- Confirm that Claude Code CLI is installed and accessible
- Validate that the current branch matches the expected pattern: `chore-issue-25-adw-2c3c1641-test-adw-workflow`

### Step 2: Document Test Workflow Execution
- Review the issue comments to understand the test execution history
- Document any errors encountered in previous test runs:
  - Unicode encoding errors (fixed in 2b08b87c)
  - Branch name extraction issues (fixed in 66624cbd)
  - Classification errors (multiple attempts)
- Verify that the current test run (2c3c1641) has successfully:
  - Classified the issue as `/chore`
  - Created the feature branch
  - Reached the planning phase

### Step 3: Validate Plan File Creation
- Ensure this plan file exists at `specs/issue-25-adw-2c3c1641-sdlc_planner-test-adw-workflow.md`
- Verify the plan follows the required format with all sections:
  - Chore Description
  - Relevant Files
  - Step by Step Tasks
  - Validation Commands
  - Notes
- Confirm the filename matches the pattern: `issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`

### Step 4: Verify State Management
- Check that the ADW state file exists and contains correct data:
  - `adw_id`: "2c3c1641"
  - `issue_number`: "25"
  - `branch_name`: "chore-issue-25-adw-2c3c1641-test-adw-workflow"
  - `plan_file`: "specs/issue-25-adw-2c3c1641-sdlc_planner-test-adw-workflow.md"
  - `issue_class`: "/chore"
- Verify state can be properly loaded and serialized to JSON for workflow chaining

### Step 5: Test Git Operations
- Confirm the current branch is checked out correctly
- Verify that the plan file will be committed with appropriate message
- Ensure commit message follows the format: `{adw_id}_sdlc_planner: ✅ Plan committed`
- Validate that pull request will be created/updated with:
  - Link to original issue #25
  - Implementation summary
  - ADW tracking ID in the description

### Step 6: Validate GitHub Integration
- Verify that issue comments are being posted with proper formatting:
  - Format: `{adw_id}_{agent_name}: {message}`
  - Example: `2c3c1641_ops: ✅ Starting planning phase`
- Confirm that the issue #25 is accessible via GitHub API
- Ensure comment posting functionality works for status updates

### Step 7: Run Validation Commands
Execute all validation commands to ensure the test chore is complete with zero regressions.

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd adws && uv run adw_tests/health_check.py` - Run ADW health check to validate system components
- `git status` - Verify git state and confirm plan file is tracked
- `git branch --show-current` - Confirm we're on the correct feature branch
- `cat specs/issue-25-adw-2c3c1641-sdlc_planner-test-adw-workflow.md` - Verify plan file exists and is readable
- `gh issue view 25 --repo $(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')` - Verify issue #25 is accessible via GitHub CLI

## Notes
- This is a meta-test: the chore itself is testing the ADW workflow system
- The plan file being created IS the deliverable for this test
- Previous test runs have identified and fixed several issues:
  - Encoding issues with JSONL parsing
  - Branch name extraction from Claude Code responses
  - Issue classification reliability
- The current branch `chore-issue-25-adw-2c3c1641-test-adw-workflow` indicates this is a test run with ADW ID `2c3c1641`
- The ADW system uses single-file Python scripts with `uv run` for execution
- All ADW scripts are located in `adws/` and use the `adw_modules/` package for shared functionality
- State management enables workflow chaining: `adw_plan.py | adw_build.py | adw_test.py`
- The test validates end-to-end functionality without requiring actual code changes to the main application
