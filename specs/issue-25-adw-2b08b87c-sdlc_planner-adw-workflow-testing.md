# Chore: Test Issue #25

## Chore Description
This is a test issue for validating the ADW (AI Developer Workflow) system's ability to handle chores. The chore involves adding comprehensive logging capabilities to the ADW system to help developers and operators monitor workflow execution, debug issues, and track the lifecycle of issue processing. This will improve observability and make it easier to troubleshoot when issues arise during automated workflow execution.

## Relevant Files
Use these files to resolve the chore:

- `adws/adw_modules/utils.py` - Utility functions module where logging utilities should be added
  - Add structured logging configuration
  - Create logging helpers for consistent log formatting
  - Add functions to log workflow state transitions
  - Implement log file rotation configuration

- `adws/adw_plan.py` - Planning phase workflow script
  - Add logging at key execution points
  - Log issue classification results
  - Log plan generation start/completion
  - Log any errors or warnings during planning

- `adws/adw_build.py` - Implementation phase workflow script
  - Add logging at key execution points
  - Log plan file discovery and loading
  - Log implementation progress
  - Log commit and push operations

- `adws/adw_test.py` - Testing phase workflow script
  - Add logging at key execution points
  - Log test execution start/completion
  - Log test results summary
  - Log any test failures with context

- `adws/adw_plan_build.py` - Combined workflow orchestration
  - Add logging for workflow orchestration
  - Log phase transitions
  - Log overall workflow status

- `adws/adw_plan_build_test.py` - Full pipeline orchestration
  - Add logging for complete pipeline execution
  - Log each phase execution
  - Log pipeline completion status

- `adws/adw_triggers/trigger_cron.py` - Cron trigger for automated monitoring
  - Add logging for monitoring cycles
  - Log issue detection and processing triggers
  - Log any errors during monitoring

- `adws/adw_triggers/trigger_webhook.py` - Webhook server for GitHub events
  - Add logging for incoming webhook events
  - Log event processing status
  - Log any webhook handling errors

- `adws/README.md` - ADW documentation
  - Add a "Logging" section to document the new logging capabilities
  - Explain log file locations and formats
  - Provide examples of common log queries
  - Document debugging techniques using logs

### New Files

- `adws/adw_modules/logger.py` - New module for centralized logging configuration
  - Configure structured logging with JSON output
  - Set up file rotation
  - Define log levels and formatting standards
  - Provide logger factory functions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create centralized logging module
- Create `adws/adw_modules/logger.py` with structured logging configuration
- Implement logger factory function that returns configured logger instances
- Configure file-based logging with rotation to `logs/adw_*.log`
- Set up both file and console output with appropriate formatting
- Use JSON formatting for file logs to enable easy parsing and analysis
- Use human-readable formatting for console logs
- Configure log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Add utility functions for logging common ADW events (state transitions, agent calls, git operations)

### Step 2: Update utils.py with logging helpers
- Import the new logger module in `adws/adw_modules/utils.py`
- Add logging helper functions for common operations
- Add context manager for logging operation duration
- Ensure backward compatibility with existing utility functions

### Step 3: Add logging to adw_plan.py
- Import logger at the top of `adws/adw_plan.py`
- Add logging when script starts and receives issue number
- Log issue classification type determination
- Log plan generation invocation
- Log successful plan creation and file path
- Log git operations (branch creation, commits)
- Log any errors with full context
- Log successful completion with summary

### Step 4: Add logging to adw_build.py
- Import logger at the top of `adws/adw_build.py`
- Add logging when build phase starts
- Log plan file discovery and loading
- Log agent invocation for implementation
- Log git operations (commits, pushes)
- Log PR updates
- Log any errors with full context
- Log successful completion with summary

### Step 5: Add logging to adw_test.py
- Import logger at the top of `adws/adw_test.py`
- Add logging when test phase starts
- Log test suite execution start
- Log test results (passed/failed counts)
- Log test failures with details
- Log git operations (commits, pushes)
- Log any errors with full context
- Log successful completion with summary

### Step 6: Add logging to orchestration scripts
- Add logging to `adws/adw_plan_build.py` for workflow orchestration
- Add logging to `adws/adw_plan_build_test.py` for full pipeline execution
- Log phase transitions and overall workflow status
- Log any errors during orchestration
- Log successful completion

### Step 7: Add logging to trigger scripts
- Add logging to `adws/adw_triggers/trigger_cron.py` for monitoring cycles
- Add logging to `adws/adw_triggers/trigger_webhook.py` for webhook events
- Log trigger activations and issue processing
- Log any errors during trigger handling

### Step 8: Create logs directory
- Ensure `logs/` directory exists (create .gitkeep file)
- Update `.gitignore` to exclude log files but keep the directory

### Step 9: Update ADW documentation
- Add a "Logging and Monitoring" section to `adws/README.md`
- Document log file locations (`logs/adw_*.log`)
- Explain log format (JSON for files, human-readable for console)
- Provide examples of common log queries using `jq` or `grep`
- Document debugging workflows using logs
- Add troubleshooting tips based on log patterns

### Step 10: Test the logging implementation
- Run `uv run adw_plan.py` with a test issue to verify logging works
- Check that log files are created in `logs/` directory
- Verify both console and file logging produce expected output
- Verify JSON log format is valid and parseable
- Test log rotation by checking file size limits work

### Step 11: Run validation commands
- Execute all validation commands to ensure the chore is complete with zero regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate no regressions in the main application
- `ls -la logs/` - Verify logs directory exists
- `cat logs/.gitkeep` - Verify .gitkeep file exists
- `grep -r "import.*logger" adws/*.py` - Verify logging is imported in ADW scripts
- `python -c "import json; json.loads(open('logs/adw_plan.log').readline())"` - Verify log files contain valid JSON (if logs exist)

## Notes
- Use Python's `logging` module as the foundation for the logging system
- Consider using `structlog` or `python-json-logger` for structured JSON logging
- Log files should rotate based on size (e.g., 10MB per file, keep 5 backups)
- Sensitive information (API keys, tokens) should NEVER be logged
- Log levels should be configurable via environment variable (default: INFO)
- Include timestamps in ISO 8601 format for all logs
- Include ADW ID in log entries to correlate logs with workflow runs
- Logs should be machine-readable (JSON) for parsing and analysis tools
- Console output should remain human-readable for interactive debugging
- The logging system should not impact performance significantly
- Consider adding log aggregation guidance for production deployments
