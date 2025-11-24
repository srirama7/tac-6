@echo off
claude -p "/classify_issue {\"number\": 31, \"title\": \"test\"}" --model sonnet --output-format stream-json --verbose --dangerously-skip-permissions > test_output.jsonl 2>&1
echo Exit code: %ERRORLEVEL%
