# Chore: ADW Workflow Testing Validation

## Chore Description
This is a test issue for validating the ADW (AI Developer Workflow) system. The chore involves adding a simple environment validation script to help developers verify their development environment setup is complete and correct before starting development. This script will check for required dependencies, configuration files, and report the status of the development environment.

## Relevant Files
Use these files to resolve the chore:

- `scripts/validate_env.sh` - New validation script that will check the development environment
  - Check for required Python version (3.10+)
  - Check for Node.js version (18+)
  - Check for uv installation
  - Check for required environment files (.env in root and app/server/)
  - Check for required API keys in environment
  - Report overall environment status

- `README.md` - Update to include information about the new validation script
  - Add a new "Environment Validation" section under Development
  - Document how to run the validation script
  - Explain what the script checks for

### New Files

- `scripts/validate_env.sh` - Shell script to validate the development environment setup

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create the environment validation script
- Create `scripts/validate_env.sh` with executable permissions
- Implement checks for:
  - Python version (3.10+)
  - Node.js version (18+)
  - uv package manager installation
  - Existence of `.env` file in root directory
  - Existence of `.env` file in `app/server/` directory
  - Presence of ANTHROPIC_API_KEY or OPENAI_API_KEY in server .env file
- Use colored output (green for pass, red for fail, yellow for warnings)
- Display a summary at the end with overall status
- Exit with appropriate exit codes (0 for success, 1 for failures)

### Step 2: Make the validation script executable
- Set executable permissions on the new script using chmod +x

### Step 3: Update README.md documentation
- Add a new "Environment Validation" subsection under the "Development" section
- Document the purpose of the validation script
- Provide usage instructions with example output
- Explain what each check validates
- Add troubleshooting guidance for common validation failures

### Step 4: Test the validation script
- Run the validation script to ensure it works correctly
- Verify all checks execute properly
- Confirm colored output displays correctly
- Test error scenarios (if possible) to verify failure detection

### Step 5: Run validation commands
- Execute all validation commands to ensure the chore is complete with zero regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `./scripts/validate_env.sh` - Run the new validation script to verify it works correctly

## Notes
- The validation script should be user-friendly and provide clear, actionable feedback
- Use POSIX-compliant shell syntax to ensure cross-platform compatibility (bash/zsh)
- The script should not modify any files, only read and report status
- Consider using version comparison for Python and Node.js version checks
- The script should help new developers quickly identify missing dependencies or configuration issues
- Exit codes should be meaningful: 0 for all checks passed, 1 for any check failed
