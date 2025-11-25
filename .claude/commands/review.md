# Code Review Against Specification

Review the implementation against the specification file and identify any issues.

## Arguments

- `$ARGUMENTS[0]`: ADW ID (workflow identifier)
- `$ARGUMENTS[1]`: Path to the specification file
- `$ARGUMENTS[2]`: Agent name (reviewer)

## Purpose

Validate that the implementation matches the specification requirements:
- Compare implemented functionality against spec requirements
- Identify any missing or incomplete features
- Check for bugs or inconsistencies
- Take screenshots of critical functionality
- Classify issues by severity

## Instructions

1. Read the specification file at `$ARGUMENTS[1]`
2. Analyze the codebase to understand what has been implemented
3. Compare implementation against each requirement in the spec
4. For any issues found:
   - Take screenshots where visual verification is relevant
   - Classify severity as: `blocker`, `tech_debt`, or `skippable`
   - Provide clear description and resolution
5. Return results as JSON

## Issue Severity Levels

- **blocker**: Critical issues that must be fixed (missing required functionality, broken features, security issues)
- **tech_debt**: Issues that should be addressed but don't block release (code quality, performance, minor bugs)
- **skippable**: Minor issues that can be deferred (style, documentation, nice-to-have)

## Report

Return ONLY a JSON object with the review results. Do not include any additional text or markdown.

### Output Structure

```json
{
  "success": boolean,
  "review_issues": [
    {
      "review_issue_number": number,
      "screenshot_path": "string (path to screenshot if taken)",
      "issue_description": "string",
      "issue_resolution": "string (suggested fix)",
      "issue_severity": "blocker" | "tech_debt" | "skippable"
    }
  ],
  "screenshots": ["array of screenshot paths taken during review"]
}
```

### Success Criteria

- `success: true` when there are NO blocker issues
- `success: false` when there are any blocker issues

### Example Output (Success)

```json
{
  "success": true,
  "review_issues": [],
  "screenshots": ["/tmp/screenshot_1.png", "/tmp/screenshot_2.png"]
}
```

### Example Output (Issues Found)

```json
{
  "success": false,
  "review_issues": [
    {
      "review_issue_number": 1,
      "screenshot_path": "/tmp/error_screenshot.png",
      "issue_description": "Export button does not download CSV file as specified",
      "issue_resolution": "Implement CSV export functionality in the export handler",
      "issue_severity": "blocker"
    },
    {
      "review_issue_number": 2,
      "screenshot_path": "",
      "issue_description": "Loading spinner continues after data loads",
      "issue_resolution": "Add state update to hide spinner on data load completion",
      "issue_severity": "tech_debt"
    }
  ],
  "screenshots": ["/tmp/error_screenshot.png", "/tmp/ui_check.png"]
}
```
