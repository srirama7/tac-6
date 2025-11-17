# Chore: Test ADW Workflow System

## Chore Description
This is a test issue for validating the ADW (AI Developer Workflow) system end-to-end. The chore involves documenting and validating the recent fixes applied to the ADW system, specifically the Unicode encoding fixes and branch name extraction improvements. This ensures the workflow can handle edge cases and operates reliably for future issues.

## Relevant Files
Use these files to resolve the chore:

- `adws/adw_modules/agent.py` - Agent execution module
  - Contains `parse_jsonl_output()` function that was fixed for UTF-8 encoding
  - Contains `convert_jsonl_to_json()` function that was updated for UTF-8 encoding
  - Handles Claude Code CLI integration and output parsing

- `adws/adw_modules/workflow_ops.py` - Core workflow operations
  - Contains branch name generation logic (around line 243)
  - Was updated to extract branch names from explanatory text using regex
  - Handles issue classification and workflow orchestration

- `adws/README.md` - ADW documentation
  - Needs update to document the fixes applied
  - Should include troubleshooting section for common encoding issues
  - Should document the branch naming format and extraction logic

- `test_claude_env.py` - Test script for Claude environment
  - Verify this test script works correctly
  - May need updates to test encoding handling

### New Files

- `adws/tests/test_encoding.py` - Test file to validate UTF-8 encoding handling
  - Test `parse_jsonl_output()` with various Unicode characters
  - Test `convert_jsonl_to_json()` with special characters
  - Ensure no regression in encoding handling

- `adws/tests/test_branch_naming.py` - Test file to validate branch name extraction
  - Test regex pattern for branch name extraction
  - Test fallback logic for extracting last line
  - Test various input formats from slash commands

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Verify encoding fixes in agent.py
- Read `adws/adw_modules/agent.py` to verify UTF-8 encoding is properly set
- Confirm `parse_jsonl_output()` uses `encoding='utf-8'` when opening files
- Confirm `convert_jsonl_to_json()` uses `encoding='utf-8'` for both read and write operations
- Verify `ensure_ascii=False` is set in `json.dump()` to preserve Unicode characters
- Document the fix in code comments if not already present

### Step 2: Verify branch name extraction fixes in workflow_ops.py
- Read `adws/adw_modules/workflow_ops.py` around line 243
- Confirm regex pattern `[a-z]+-issue-\\d+-adw-[a-f0-9]+-[a-z0-9-]+` is implemented
- Verify fallback logic extracts last non-empty line if regex doesn't match
- Ensure the logic handles explanatory text from slash commands properly
- Add comments documenting the extraction logic if not already present

### Step 3: Create encoding test suite
- Create `adws/tests/` directory if it doesn't exist
- Create `adws/tests/test_encoding.py` with comprehensive encoding tests
- Test parsing JSONL files with various Unicode characters (emoji, special chars, non-Latin scripts)
- Test JSON conversion with UTF-8 encoded content
- Verify no 'charmap' codec errors occur
- Use pytest framework for test structure

### Step 4: Create branch naming test suite
- Create `adws/tests/test_branch_naming.py` with branch name extraction tests
- Test regex extraction with valid branch names
- Test handling of explanatory text before branch name
- Test fallback logic with edge cases
- Test handling of invalid inputs gracefully
- Use pytest framework for test structure

### Step 5: Update ADW documentation
- Add a "Recent Fixes" or "Troubleshooting" section to `adws/README.md`
- Document the Unicode encoding fix with the error message and solution
- Document the branch name extraction fix with example problematic input
- Add guidance on handling encoding issues in future development
- Add examples of proper branch name format
- Include debugging tips for workflow issues

### Step 6: Validate test_claude_env.py script
- Read and review `test_claude_env.py` in the root directory
- Run the script to ensure it executes without errors
- Verify it properly tests the Claude Code environment
- Update or fix if any issues are found

### Step 7: Run the new test suites
- Execute `uv run pytest adws/tests/test_encoding.py -v` to validate encoding handling
- Execute `uv run pytest adws/tests/test_branch_naming.py -v` to validate branch name extraction
- Ensure all tests pass
- Fix any failing tests

### Step 8: Create validation documentation
- Create or update `.github/ISSUE_TEMPLATE/test-adw.md` template for testing ADW workflow
- Document the testing process for future ADW workflow validation
- Include checklist of what to verify
- Add examples of successful workflow execution

### Step 9: Run all validation commands
- Execute all validation commands to ensure the chore is complete with zero regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate no regressions in main application
- `uv run pytest adws/tests/test_encoding.py -v` - Validate encoding handling tests
- `uv run pytest adws/tests/test_branch_naming.py -v` - Validate branch naming tests
- `cd adws && uv run python test_claude_env.py` - Validate Claude environment test script (if applicable)
- `git status` - Verify all changes are properly staged

## Notes
- The encoding fix addresses the error: `'charmap' codec can't decode byte 0x8f in position 5185: character maps to <undefined>`
- The branch name extraction fix addresses the "Filename too long" error caused by treating explanatory text as branch name
- Always use UTF-8 encoding when reading/writing files in Python on Windows to avoid codec errors
- Branch names follow format: `{type}-issue-{number}-adw-{adw_id}-{descriptive-name}`
- Regex pattern must match the branch naming convention exactly
- Fallback logic should only trigger when regex doesn't match
- Tests should cover both happy path and edge cases
- Documentation should help future developers avoid similar issues
- This test issue validates the workflow can handle the complete cycle: classify, plan, build, test
