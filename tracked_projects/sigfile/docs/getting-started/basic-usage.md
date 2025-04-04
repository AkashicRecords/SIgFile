# Basic Usage Guide

## Overview
This guide covers the basic usage of SigFile CLI commands for managing your development environment and tracking changes. The CLI is built on a base command structure that provides consistent functionality across all commands.

## Common Commands

### 1. Recording Decisions
```bash
# Record a new decision with all parameters
sigfile decision create "Title of Decision" "Description" --type architectural --priority high

# Record a decision in interactive mode
sigfile decision create

# View a specific decision
sigfile decision view <decision_id>

# List all decisions
sigfile decision list

# List decisions with specific type
sigfile decision list --type architectural
```

### 2. Managing Development Environment
```bash
# Check current permissions and status
sigfile dev check

# Update permissions
sigfile dev update

# View permission history
sigfile dev history
```

### 3. Creating Handoff Documents
```bash
# Create a new handoff document
sigfile handoff create "Title" "Description"

# Create a handoff with affected code blocks
sigfile handoff create "Title" "Description" --files "path/to/file1.py" "path/to/file2.py"

# View a handoff document
sigfile handoff view <handoff_id>

# List all handoffs
sigfile handoff list
```

## Examples

### Recording a Decision
```bash
# Basic decision
sigfile decision create "Implement CLI Package" "Create a separate Python package for the SigFile CLI to improve maintainability and distribution."

# Decision with type and priority
sigfile decision create "Add Unit Testing" "Implement comprehensive unit tests for the CLI package" --type technical --priority high

# Interactive mode
sigfile decision create
# Follow the prompts to enter title, description, type, and priority
```

### Checking Development Environment
```bash
# Basic check
sigfile dev check
# Output will show:
# - Current permissions
# - Environment status
# - Any issues that need attention

# Update permissions
sigfile dev update
# Follow the prompts to update permissions as needed
```

### Creating a Handoff Document
```bash
# Basic handoff
sigfile handoff create "CLI Package Implementation" "Documentation of the CLI package implementation and changes made."

# Handoff with affected files
sigfile handoff create "Base Command Implementation" "Implementation of the BaseCommand class" --files "sigfile_cli/utils/base.py" "sigfile_cli/commands/decision.py"
```

## Base Command Features
All commands inherit from a base command class that provides:
- Standardized file operations
- Error handling
- Record management
- Metadata tracking
- Developer ID detection

## Best Practices
1. Always provide clear, descriptive titles for decisions and handoffs
2. Include relevant context and reasoning in descriptions
3. Use the CLI commands consistently to maintain proper tracking
4. Regularly check your development environment status
5. Use interactive mode for complex operations
6. Include affected files in handoff documents when relevant

## Next Steps
For more advanced usage and features, see the [Advanced Usage](../advanced/ai-sessions.md) guide. 