# ADW Simple Workflow Flowchart

## Overview
ADW (Application Development Workflow) is an automated Plan-Build-Test system that processes GitHub issues through three main phases.

## Swim Lane Diagram - Actor Interactions

This diagram shows how Human, GitHub, ADW Python scripts, and Claude Code interact throughout the workflow.

```mermaid
%%{init: {'theme':'base'}}%%
graph TB
    subgraph Human[" HUMAN "]
        H1[Create GitHub Issue]
        H9[Review Pull Request]
        H10[Merge or Request Changes]
    end

    subgraph GitHub[" GITHUB "]
        G1[Store Issue #123<br/>Title & Description]
        G2[Send Webhook Event]
        G4[Receive Branch<br/>feat-issue-123-adw-a1b2c3d4]
        G7[Store Implementation<br/>Code Changes]
        G8[Update PR with<br/>Test Results]
        G9[Display PR for Review]
    end

    subgraph ADWPython[" ADW PYTHON SCRIPTS "]
        A1[Generate ADW ID<br/>a1b2c3d4]
        A2[Initialize State File<br/>adw_state.json]
        A3[Run adw_plan.py<br/>Orchestrate Planning]
        A4[Create Git Branch]
        A5[Save Plan to State]
        A7[Run adw_build.py<br/>Orchestrate Build]
        A8[Load State & Checkout]
        A9[Commit & Push Code]
        A10[Run adw_test.py<br/>Orchestrate Tests]
        A11[Parse Test Results]
        A12[Retry Failed Tests<br/>Up to 4x unit, 2x E2E]
        A13[Commit & Push Results]
        A14[Update PR Status]
    end

    subgraph ClaudeCode[" CLAUDE CODE AI "]
        C1[Classify Issue<br/>/feature /bug /chore]
        C2[Generate Branch Name]
        C3[Create Implementation Plan<br/>sdlc_planner agent]
        C4[Write Plan Document]
        C5[Read Plan File]
        C6[Implement Solution<br/>sdlc_implementor agent]
        C7[Write Code Changes]
        C8[Run Unit Tests<br/>test_runner agent]
        C9[Fix Failed Tests<br/>resolve_failed_test]
        C10[Run E2E Tests<br/>e2e_test_runner agent]
        C11[Fix Failed E2E Tests<br/>resolve_failed_e2e_test]
    end

    %% Phase 0: Initialization
    H1 --> G1
    G1 --> G2
    G2 --> A1
    A1 --> A2

    %% Phase 1: Planning
    A2 --> A3
    A3 --> C1
    C1 --> A3
    A3 --> C2
    C2 --> A3
    A3 --> A4
    A4 --> C3
    C3 --> C4
    C4 --> A5
    A5 --> G4
    G4 --> A7

    %% Phase 2: Building
    A7 --> A8
    A8 --> C5
    C5 --> C6
    C6 --> C7
    C7 --> A9
    A9 --> G7

    %% Phase 3: Testing
    G7 --> A10
    A10 --> C8
    C8 --> A11
    A11 --> A12
    A12 --> C9
    C9 --> A12
    A12 --> C10
    C10 --> A11
    A11 --> A12
    A12 --> C11
    C11 --> A12
    A12 --> A13
    A13 --> G8

    %% Final Review
    G8 --> A14
    A14 --> G9
    G9 --> H9
    H9 --> H10

    style H1 fill:#FFE5B4
    style H9 fill:#FFE5B4
    style H10 fill:#98FB98

    style G1 fill:#87CEEB
    style G2 fill:#87CEEB
    style G4 fill:#87CEEB
    style G7 fill:#87CEEB
    style G8 fill:#87CEEB
    style G9 fill:#87CEEB

    style A1 fill:#F0E68C
    style A2 fill:#F0E68C
    style A3 fill:#DDA0DD
    style A4 fill:#DDA0DD
    style A5 fill:#DDA0DD
    style A7 fill:#F0E68C
    style A8 fill:#F0E68C
    style A9 fill:#F0E68C
    style A10 fill:#FFB6C1
    style A11 fill:#FFB6C1
    style A12 fill:#FFB6C1
    style A13 fill:#FFB6C1
    style A14 fill:#98FB98

    style C1 fill:#9370DB
    style C2 fill:#9370DB
    style C3 fill:#9370DB
    style C4 fill:#9370DB
    style C5 fill:#9370DB
    style C6 fill:#9370DB
    style C7 fill:#9370DB
    style C8 fill:#9370DB
    style C9 fill:#9370DB
    style C10 fill:#9370DB
    style C11 fill:#9370DB
```

### Actor Responsibilities

**Human**
- Creates GitHub issues describing features, bugs, or chores
- Triggers ADW workflow manually or via webhook/cron
- Reviews and merges the final pull request

**GitHub**
- Stores issues, code repositories, and documentation
- Sends webhook events on issue creation
- Hosts branches, pull requests, and issue comments
- Provides API access to issue data

**ADW Python**
- Orchestrates the three-phase workflow (Plan, Build, Test)
- Manages state persistence across phases
- Handles git operations (branch, commit, push)
- Parses and processes test results
- Implements retry logic for failed tests
- Updates GitHub with progress and results

**Claude Code**
- Classifies issues into feature/bug/chore categories
- Generates appropriate branch names
- Creates detailed implementation plans
- Implements the solution based on the plan
- Runs and analyzes test results
- Automatically fixes failing tests
- Provides AI-powered development assistance

## High-Level Flow

```mermaid
flowchart TD
    Start([GitHub Issue]) --> Init[Initialize ADW<br/>Generate unique ID<br/>Create state file]

    Init --> Plan[PLAN PHASE<br/>adw_plan.py]
    Plan --> Build[BUILD PHASE<br/>adw_build.py]
    Build --> Test[TEST PHASE<br/>adw_test.py]
    Test --> End([Pull Request Ready])

    style Start fill:#90EE90
    style Init fill:#87CEEB
    style Plan fill:#DDA0DD
    style Build fill:#F0E68C
    style Test fill:#FFB6C1
    style End fill:#98FB98
```

## Three Phase Workflow

```mermaid
flowchart LR
    subgraph Phase1[" PLAN PHASE "]
        P1[Classify Issue<br/>/feature /bug /chore]
        P2[Generate Branch Name]
        P3[Create Implementation Plan]
        P1 --> P2 --> P3
    end

    subgraph Phase2[" BUILD PHASE "]
        B1[Read Plan]
        B2[Implement Solution]
        B3[Commit Changes]
        B1 --> B2 --> B3
    end

    subgraph Phase3[" TEST PHASE "]
        T1[Run Unit Tests]
        T2[Fix Failed Tests]
        T3[Run E2E Tests]
        T4[Fix Failed E2E Tests]
        T1 --> T2 --> T3 --> T4
    end

    Phase1 --> Phase2 --> Phase3

    style Phase1 fill:#DDA0DD20
    style Phase2 fill:#F0E68C20
    style Phase3 fill:#FFB6C120
```

## Detailed Workflow

```mermaid
flowchart TD
    Start([GitHub Issue #123]) --> Trigger{How Triggered?}

    Trigger -->|Manual| M[uv run adw_plan_build_test.py 123]
    Trigger -->|Webhook| W[GitHub webhook event]
    Trigger -->|Cron| C[Scheduled monitoring]

    M --> Init
    W --> Init
    C --> Init

    Init[Generate ADW ID: a1b2c3d4<br/>Create state file] --> PlanStart

    subgraph Planning[" PLANNING PHASE "]
        PlanStart[Fetch issue details] --> Classify[Classify as /feature, /bug, or /chore]
        Classify --> Branch[Generate branch name<br/>feat-issue-123-adw-a1b2c3d4-name]
        Branch --> CreateBranch[Create git branch]
        CreateBranch --> GenPlan[Run sdlc_planner agent<br/>Generate implementation plan]
        GenPlan --> SavePlan[Save to specs/issue-123-adw-a1b2c3d4-*.md]
        SavePlan --> CommitPlan[Commit & push<br/>Create PR]
    end

    CommitPlan --> BuildStart

    subgraph Building[" BUILD PHASE "]
        BuildStart[Load state & checkout branch] --> ReadPlan[Read plan file]
        ReadPlan --> Implement[Run sdlc_implementor agent<br/>Implement solution]
        Implement --> CommitImpl[Commit & push changes<br/>Update PR]
    end

    CommitImpl --> TestStart

    subgraph Testing[" TEST PHASE "]
        TestStart[Checkout branch] --> UnitTest[Run unit tests<br/>pytest via /test]
        UnitTest --> UnitPass{All Pass?}
        UnitPass -->|Yes| E2ETest[Run E2E tests<br/>/test_e2e]
        UnitPass -->|No| ResolveUnit[Attempt to fix<br/>/resolve_failed_test]
        ResolveUnit --> RetryUnit{Retry?<br/>< 4 attempts}
        RetryUnit -->|Yes| UnitTest
        RetryUnit -->|No| Failed

        E2ETest --> E2EPass{All Pass?}
        E2EPass -->|Yes| Success
        E2EPass -->|No| ResolveE2E[Attempt to fix<br/>/resolve_failed_e2e_test]
        ResolveE2E --> RetryE2E{Retry?<br/>< 2 attempts}
        RetryE2E -->|Yes| E2ETest
        RetryE2E -->|No| Failed
    end

    Success[Commit test results<br/>Push & update PR<br/>Post success comment] --> End([PR Ready for Review])
    Failed[Commit test results<br/>Push & update PR<br/>Post failure comment] --> End

    style Start fill:#90EE90
    style Init fill:#87CEEB
    style Planning fill:#DDA0DD20
    style Building fill:#F0E68C20
    style Testing fill:#FFB6C120
    style Success fill:#98FB98
    style Failed fill:#FF6B6B
    style End fill:#FFB6C1
```

## Key Components

### State Management
```json
{
  "adw_id": "a1b2c3d4",
  "issue_number": "123",
  "issue_class": "/feature",
  "branch_name": "feat-issue-123-adw-a1b2c3d4-name",
  "plan_file": "specs/issue-123-adw-a1b2c3d4-name.md"
}
```

### Trigger Methods
1. **Manual**: `uv run adw_plan_build_test.py ISSUE_NUMBER`
2. **Webhook**: GitHub webhook on issue creation
3. **Cron**: Scheduled monitoring for new/tagged issues

### Test Retry Logic
- **Unit Tests**: Up to 4 attempts with automatic resolution
- **E2E Tests**: Up to 2 attempts with automatic resolution
- **E2E Requirement**: Only runs if unit tests pass

### Output
- Git branch with changes
- Pull request to main branch
- Issue comments tracking progress
- Committed plan and implementation
- Test results

## Quick Summary

1. **Issue Created** → ADW triggered
2. **Plan**: Classify → Branch → Generate plan → Commit
3. **Build**: Load plan → Implement → Commit
4. **Test**: Unit tests → E2E tests → Auto-fix failures → Commit
5. **Result**: PR ready with all changes and test results
