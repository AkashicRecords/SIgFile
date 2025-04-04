# Decision CLI

The Decision CLI is a command-line interface for managing development decisions in SigFile. It allows you to create, update, and track decisions made during the development process, providing a comprehensive record of your development history.

## Overview

The Decision CLI provides commands for:

1. Creating new unresolved decisions
2. Updating existing decisions with outcomes
3. Viewing decision history
4. Linking decisions to code changes

## Usage

### Command Line Interface

The Decision CLI is accessed through the main SigFile CLI:

```bash
# Create a new unresolved decision
python -m src.scripts.cli decision -n -t "Decision Title" -d "Decision Description" -c "Decision Context"

# Update an existing decision with an outcome
python -m src.scripts.cli decision -t "Decision Title" -o "Decision Outcome"
```

### Command Options

- `-n, --new`: Create a new unresolved decision
- `-t, --title`: Decision title (required)
- `-d, --description`: Decision description
- `-c, --context`: Decision context
- `-o, --outcome`: Decision outcome

### Examples

#### Creating a New Decision

```bash
# Create a new decision about file structure
python -m src.scripts.cli decision -n -t "Update directory and file structure" -d "Reorganize project directories for better code organization" -c "Current structure is becoming unwieldy as the project grows"
```

#### Updating a Decision with an Outcome

```bash
# Update a decision with its outcome
python -m src.scripts.cli decision -t "Update directory and file structure" -o "Implemented new structure with separate directories for features, tests, and documentation"
```

## Decision Structure

Each decision is recorded with the following information:

1. **Title**: A concise description of the decision
2. **Description**: Detailed explanation of the decision
3. **Context**: Background information and rationale
4. **Outcome**: The result of the decision (if resolved)
5. **Timestamp**: When the decision was made
6. **Related Changes**: Code changes linked to this decision

## Integration with Change Tracking

The Decision CLI integrates with SigFile's change tracking system to link decisions with code changes:

```python
from src.scripts.track_change import OptimizedCapture

# Create a capture instance
capture = OptimizedCapture("project_name")

# Record a development decision
capture._record_development_decision(
    "Decision Type",
    "Decision Title",
    "Decision Context",
    "Decision Outcome",
    related_changes=["file1.py", "file2.py"]
)
```

## Best Practices

1. **Be Specific**: Use clear, specific titles and descriptions for your decisions.
2. **Provide Context**: Include enough context to understand why the decision was made.
3. **Link Changes**: Link decisions to the code changes they influenced.
4. **Update Outcomes**: Update decisions with outcomes once they are resolved.
5. **Review Regularly**: Periodically review your decision history to track progress.

## Related Documentation
- [Decision Tracking](advanced/decision-tracking.md) - Advanced decision tracking features
- [Change Management](features/change-management.md) - How changes are tracked and managed
- [Project Organization](features/project-organization.md) - How projects are organized in SigFile 