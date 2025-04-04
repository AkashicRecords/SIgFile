# SigFile CLI Architecture

## Overview

The SigFile CLI is designed as a separate Python package that provides a command-line interface for managing developer signatures and decisions. The architecture follows a modular design with a focus on code reuse and maintainability.

## Package Structure

```
sigfile-cli/
├── setup.py                 # Package configuration
├── README.md                # Package documentation
├── requirements.txt         # Dependencies
├── sigfile_cli/             # Main package directory
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Main CLI entry point
│   ├── commands/            # Command implementations
│   │   ├── __init__.py      # Commands package
│   │   ├── decision.py      # Decision command
│   │   ├── devenv.py        # Development environment command
│   │   └── ...              # Other commands
│   ├── utils/               # Utility modules
│   │   ├── __init__.py      # Utils package
│   │   ├── base.py          # Base command class
│   │   ├── error_handling.py # Error handling
│   │   ├── developer_id.py  # Developer ID management
│   │   └── ...              # Other utilities
│   └── man/                 # Manual pages
│       ├── decision.man     # Decision command manual
│       ├── devenv.man       # Development environment manual
│       └── ...              # Other manuals
└── tests/                   # Test suite
    ├── __init__.py          # Tests package
    ├── test_cli.py          # CLI tests
    ├── test_commands.py     # Command tests
    └── ...                  # Other tests
```

## Core Components

### BaseCommand Class

The `BaseCommand` class in `utils/base.py` provides common functionality for all commands:

- File operations (save/load JSON)
- Directory management
- Field validation
- Record listing

This class reduces code duplication and ensures consistent behavior across commands.

### Command Classes

Each command is implemented as a class that inherits from `BaseCommand`:

- `DecisionCommand`: Manages development decisions
- `DevEnvCommand`: Manages development environment permissions
- Other commands follow the same pattern

### Error Handling

The error handling system provides:

- Custom exceptions for different error types
- Consistent error messages with manual page references
- A decorator for handling errors across commands

### Developer ID Management

The developer ID system ensures consistency by:

- Getting the ID from git config first
- Falling back to system login if git config is not available
- Including the ID in all operations

## Command Execution Flow

1. User invokes a command (e.g., `sigfile decision -n -t "Title"`)
2. The CLI module parses arguments and validates them
3. If in interactive mode, prompts the user for missing information
4. Shows the final command for review
5. Executes the command using the appropriate command class
6. Handles any errors and displays appropriate messages

## Extension Points

The architecture is designed to be easily extended:

1. Add new commands by creating classes that inherit from `BaseCommand`
2. Add new utilities in the `utils` directory
3. Add new manual pages in the `man` directory

## Installation and Usage

The CLI can be installed with pip:

```bash
pip install sigfile-cli
```

Usage examples:

```bash
# Create a decision
sigfile decision -n -t "Implement caching" -y performance -p high

# Interactive mode
sigfile decision

# View manual
sigfile decision -man
``` 