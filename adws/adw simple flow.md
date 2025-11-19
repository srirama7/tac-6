# ADW Simple Workflow - Swim Lane Diagram

## Overview
ADW (Application Development Workflow) is an automated Plan-Build-Test system that processes GitHub issues through three main phases.

## Swim Lane Diagram

This diagram shows the workflow across five swim lanes representing Human, GitHub, Git, ADW Python, and Claude Code.

```mermaid
graph TD
    subgraph HUMAN["👤 HUMAN"]
        H1[Create GitHub Issue<br/>Feature/Bug/Chore]
        H3[Review PR]
        H4[Merge Changes]
    end

    subgraph GITHUB["🌐 GITHUB"]
        G1[Issue Stored<br/>#123]
        G4[Store Branch<br/>feat-issue-123-adw-xyz]
        G5[Store Plan<br/>specs/*.md]
        G6[Create Pull<br/>Request]
        G7[Store Code<br/>Implementation]
        G8[Store Test<br/>Results]
        G9[PR Ready for<br/>Review]
    end

    subgraph GIT["📂 GIT"]
        GT1[Create Branch<br/>feat-issue-123]
        GT2[Checkout Branch<br/>feat-issue-123]
        GT3[Commit Plan<br/>specs/*.md]
        GT4[Push Plan<br/>to Remote]
        GT5[Commit Code<br/>Implementation]
        GT6[Push Code<br/>to Remote]
        GT7[Commit Tests<br/>Results & Fixes]
        GT8[Push Tests<br/>to Remote]
    end

    subgraph PYTHON["🐍 ADW PYTHON"]
        P1[Generate ID<br/>a1b2c3d4]
        P3[Run adw_plan.py<br/>Orchestrate Planning]
        P4[Prepare Branch<br/>Info]
        P5[Save Plan<br/>to State]
        P6[Run adw_build.py<br/>Orchestrate Build]
        P7[Load State]
        P8[Run adw_test.py<br/>Orchestrate Testing]
        P9[Parse Test<br/>Results]
        P10[Retry Logic<br/>4x Unit, 2x E2E]
        P11[Update PR<br/>Status]
    end

    subgraph CLAUDE["🤖 CLAUDE CODE AI"]
        C1[Classify Issue<br/>/feature /bug /chore]
        C2[Generate Branch<br/>Name]
        C3[Create Plan<br/>sdlc_planner]
        C4[Write Plan<br/>Document]
        C5[Read Plan<br/>File]
        C6[Implement Code<br/>sdlc_implementor]
        C7[Write Code<br/>Changes]
        C8[Run Unit Tests<br/>test_runner]
        C9[Fix Failed<br/>Unit Tests]
        C10[Run E2E Tests<br/>e2e_test_runner]
        C11[Fix Failed<br/>E2E Tests]
    end

    %% Flow connections
    H1 --> G1
    G1 --> P1

    P1 --> P3

    P3 --> C1
    C1 --> P3
    P3 --> C2
    C2 --> P4

    P4 --> GT1
    GT1 --> C3
    C3 --> C4
    C4 --> P5

    P5 --> GT3
    GT3 --> GT4
    GT4 --> G4
    G4 --> G5
    G5 --> G6

    G6 --> P6
    P6 --> P7
    P7 --> GT2
    GT2 --> C5

    C5 --> C6
    C6 --> C7
    C7 --> GT5

    GT5 --> GT6
    GT6 --> G7
    G7 --> P8

    P8 --> C8
    C8 --> P9
    P9 --> P10

    P10 --> C9
    C9 --> P10
    P10 --> C10

    C10 --> P9
    P9 --> P10
    P10 --> C11
    C11 --> P10

    P10 --> GT7
    GT7 --> GT8
    GT8 --> G8
    G8 --> P11

    P11 --> G9
    G9 --> H3
    H3 --> H4

    classDef humanStyle fill:#FFE5B4,stroke:#FF8C00,stroke-width:2px,color:#000
    classDef githubStyle fill:#87CEEB,stroke:#4682B4,stroke-width:2px,color:#000
    classDef gitStyle fill:#98FB98,stroke:#228B22,stroke-width:2px,color:#000
    classDef pythonStyle fill:#F0E68C,stroke:#DAA520,stroke-width:2px,color:#000
    classDef claudeStyle fill:#DDA0DD,stroke:#9370DB,stroke-width:2px,color:#000

    class H1,H3,H4 humanStyle
    class G1,G4,G5,G6,G7,G8,G9 githubStyle
    class GT1,GT2,GT3,GT4,GT5,GT6,GT7,GT8 gitStyle
    class P1,P3,P4,P5,P6,P7,P8,P9,P10,P11 pythonStyle
    class C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11 claudeStyle
```

## Workflow Flow Across Lanes

### Phase 0: Initialization
1. **HUMAN** → Creates issue
2. **GITHUB** → Stores issue
3. **ADW PYTHON** → Generates unique ADW ID

### Phase 1: Planning
1. **ADW PYTHON** → Runs adw_plan.py, fetches issue data from GitHub
2. **CLAUDE CODE** → Classifies issue, generates branch name
3. **ADW PYTHON** → Prepares branch information
4. **GIT** → Creates new feature branch
5. **CLAUDE CODE** → Creates implementation plan (sdlc_planner)
6. **ADW PYTHON** → Saves plan to state
7. **GIT** → Commits and pushes plan to remote
8. **GITHUB** → Stores branch, plan file, creates pull request

### Phase 2: Building
1. **ADW PYTHON** → Runs adw_build.py, loads state
2. **GIT** → Checks out feature branch
3. **CLAUDE CODE** → Reads plan, implements solution (sdlc_implementor)
4. **GIT** → Commits and pushes implementation to remote
5. **GITHUB** → Stores code changes

### Phase 3: Testing
1. **ADW PYTHON** → Runs adw_test.py
2. **CLAUDE CODE** → Runs unit tests (test_runner)
3. **ADW PYTHON** → Parses results, manages retry logic
4. **CLAUDE CODE** → Fixes failed tests (up to 4 attempts)
5. **CLAUDE CODE** → Runs E2E tests (e2e_test_runner)
6. **CLAUDE CODE** → Fixes failed E2E tests (up to 2 attempts)
7. **GIT** → Commits and pushes test results to remote
8. **GITHUB** → Stores test results
9. **ADW PYTHON** → Updates PR status

### Phase 4: Review
1. **GITHUB** → Displays PR ready for review
2. **HUMAN** → Reviews and merges PR

## Actor Responsibilities

| Actor | Role | Key Activities |
|-------|------|----------------|
| **👤 HUMAN** | Initiator & Reviewer | Creates issues, triggers workflow, reviews and merges PRs |
| **🌐 GITHUB** | Storage & Integration | Stores issues/code/PRs, sends webhooks, provides API access |
| **📂 GIT** | Version Control | Creates branches, commits changes, pushes to remote |
| **🐍 ADW PYTHON** | Orchestrator | Manages workflow phases, state persistence, retry logic |
| **🤖 CLAUDE CODE AI** | Developer | Classifies, plans, implements, tests, and fixes code automatically |

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

## Quick Summary

**HUMAN** creates issue → **GITHUB** stores → **ADW PYTHON** orchestrates → **CLAUDE CODE** plans → **GIT** creates branch & commits → **GITHUB** stores → **ADW PYTHON** manages → **GIT** checks out → **CLAUDE CODE** implements → **GIT** commits & pushes → **GITHUB** stores → **ADW PYTHON** orchestrates testing → **CLAUDE CODE** tests & fixes → **GIT** commits & pushes → **GITHUB** updates → **HUMAN** reviews & merges
