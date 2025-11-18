# Chore: Test Issue #25 - ADW Workflow Testing

## Chore Description
This chore validates the complete AI Developer Workflow (ADW) system end-to-end. The ADW system is an automation framework that integrates GitHub issues with Claude Code CLI to classify issues, generate implementation plans, implement solutions, and create pull requests. This test ensures all workflow phases work correctly without errors including issue classification, branch generation, plan creation, and git operations.

Based on the issue history, previous test runs have encountered and resolved several issues:
- Unicode encoding errors in JSONL parsing (fixed with UTF-8 encoding)
- Branch name extraction from Claude Code responses (fixed with regex extraction)
- Issue classification command validation

This test validates that all these fixes work together in a complete workflow run.

## Relevant Files
Use these files to resolve the chore:

- `adws/adw_plan.py` - Main planning workflow script that orchestrates issue classification, branch creation, plan generation, and PR creation
- `adws/adw_build.py` - Build/implementation workflow script that executes the generated plan
- `adws/adw_test.py` - Testing workflow script that validates implementations
- `adws/adw_plan_build.py` - Convenience script that chains planning and building phases
- `adws/adw_plan_build_test.py` - Full pipeline script that chains all three phases (plan, build, test)

- `adws/adw_modules/workflow_ops.py` - Core workflow operations including:
  - Issue classification (`classify_issue`)
  - Branch name generation (`generate_branch_name`)
  - Plan building (`build_plan`)
  - Commit message creation (`create_commit`)

- `adws/adw_modules/agent.py` - Claude Code CLI integration module with:
  - Agent execution (`prompt_claude_code`, `execute_template`)
  - JSONL parsing with UTF-8 encoding (`parse_jsonl_output`)
  - JSON conversion (`convert_jsonl_to_json`)

- `adws/adw_modules/git_ops.py` - Git operations including:
  - Branch creation (`create_branch`)
  - Commit operations (`commit_changes`)
  - PR finalization (`finalize_git_operations`)

- `adws/adw_modules/github.py` - GitHub API integration for:
  - Issue fetching (`fetch_issue`)
  - Comment posting (`make_issue_comment`)
  - Repository information (`get_repo_url`, `extract_repo_path`)

- `adws/adw_modules/state.py` - ADW state management for workflow chaining
- `adws/adw_modules/data_types.py` - Pydantic models for type safety
- `adws/adw_modules/utils.py` - Utility functions including logger setup and ADW ID generation

- `.claude/commands/chore.md` - Chore planning slash command template
- `.claude/commands/classify_issue.md` - Issue classification slash command
- `.claude/commands/generate_branch_name.md` - Branch name generation slash command
- `.claude/commands/commit.md` - Commit message generation slash command

- `adws/adw_tests/test_agents.py` - Agent model testing (opus/sonnet)
- `adws/adw_tests/test_adw_test_e2e.py` - E2E test workflow validation

- `README.md` - Project overview and ADW documentation
- `adws/README.md` - Detailed ADW system documentation with usage examples

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Verify environment setup
- Confirm all required environment variables are set:
  - `ANTHROPIC_API_KEY` - For Claude Code CLI
  - `CLAUDE_CODE_PATH` - Path to Claude executable (optional, defaults to "claude")
  - `GITHUB_REPO_URL` - GitHub repository URL
  - `GITHUB_PAT` - GitHub personal access token (optional if using gh auth login)
- Verify Claude Code CLI is installed and accessible
- Verify GitHub CLI is authenticated (run `gh auth status`)
- Ensure Python environment with uv is working

### Step 2: Validate ADW workflow scripts execute without errors
- Run the planning phase for this test issue to ensure:
  - Issue is fetched correctly from GitHub API
  - Issue is classified as `/chore` correctly
  - Branch name is generated in correct format: `chore-issue-25-adw-9ede8ca6-test-adw-workflow`
  - Implementation plan is created successfully
  - Plan file is saved to specs directory with correct naming
  - Git commit is created for the plan
  - Pull request is created successfully
- Verify all ADW state transitions are logged correctly
- Confirm GitHub issue comments are posted at each workflow step
- Ensure JSONL output is parsed correctly with UTF-8 encoding
- Validate branch name extraction from Claude Code responses

### Step 3: Verify slash command templates are working
- Ensure `/classify_issue` command returns valid issue class (`/chore`, `/bug`, or `/feature`)
- Validate `/generate_branch_name` command returns properly formatted branch name
- Confirm `/commit` command generates semantic commit messages
- Test that `/chore` planning command creates plans following the required format

### Step 4: Validate state management and workflow chaining
- Verify `ADWState` correctly saves and loads state between workflow phases
- Confirm state contains all required fields:
  - `adw_id` - Unique workflow identifier
  - `issue_number` - GitHub issue number
  - `branch_name` - Generated git branch name
  - `plan_file` - Path to generated plan file
  - `issue_class` - Classified issue type
- Ensure state persists across script invocations

### Step 5: Test error handling and edge cases
- Verify encoding errors are handled correctly (UTF-8 encoding in file operations)
- Confirm branch name extraction handles multiline Claude responses
- Validate issue classification handles empty or invalid responses
- Test that workflow gracefully handles API failures
- Ensure all error messages are posted to GitHub issue comments

### Step 6: Validate git operations
- Confirm branch is created successfully without "filename too long" errors
- Verify commits are created with proper semantic commit messages
- Ensure pull request is created with correct title and body
- Validate branch is pushed to remote repository
- Confirm PR links back to original issue

### Step 7: Document test results
- Create a summary of the test execution
- Document any errors encountered and their resolutions
- Verify all workflow phases completed successfully
- Confirm plan file was created in correct format
- Validate all GitHub issue comments were posted correctly

### Step 8: Run validation commands
- Execute all validation commands to ensure zero regressions
- Verify the complete ADW workflow runs successfully
- Confirm all test scripts execute without errors

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd adws && uv run adw_tests/test_agents.py` - Test that opus and sonnet models work with Claude Code agent
- `cd adws && uv run adw_plan.py 25 9ede8ca6` - Run the planning phase to validate workflow executes successfully
- `ls -la ../specs/issue-25-adw-9ede8ca6-*` - Verify the plan file was created
- `cat ../specs/issue-25-adw-9ede8ca6-*.md` - Verify plan file contains correct format and content
- `gh issue view 25 --comments` - Verify GitHub issue has workflow status comments
- `git branch --list "*issue-25*"` - Verify branch was created
- `gh pr list --head chore-issue-25-adw-9ede8ca6-test-adw-workflow` - Verify PR was created for the test issue

## Notes
- This is a meta-test issue - it tests the ADW workflow system itself rather than implementing a feature
- The issue has gone through multiple iterations (ADW IDs: 2b08b87c, 66624cbd, bb2452ad, 795abd82, 7861332b, 9ede8ca6) with various fixes applied
- Previous fixes include:
  - UTF-8 encoding for JSONL file operations (adw_modules/agent.py)
  - Regex-based branch name extraction from Claude Code responses (adw_modules/workflow_ops.py line 243)
  - Issue classification validation
- The ADW workflow consists of three main phases:
  1. **Planning** (adw_plan.py) - Classify, branch, plan, commit, PR
  2. **Building** (adw_build.py) - Implement the plan
  3. **Testing** (adw_test.py) - Run tests and validate
- Each phase can run independently or be chained using state management
- The test validates that fixes from previous iterations work correctly together
- Success criteria: Complete workflow execution without errors, plan file created, PR created, all GitHub comments posted
