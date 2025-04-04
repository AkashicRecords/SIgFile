# SigFile CLI

Command Line Interface for SigFile - Developer Signature Tracking

## Installation

```bash
# Install from PyPI
pip install sigfile-cli

# Or install from source
git clone https://github.com/yourusername/sigfile-cli.git
cd sigfile-cli
pip install -e .
```

## Usage

The SigFile CLI provides commands for managing developer signatures and decisions:

### Base Command Features

All commands inherit from the base command class, providing:
- Standardized file operations
- Error handling and validation
- Record listing and management
- Metadata tracking
- Developer ID detection

### Decision Command

Create a new decision:
```bash
sigfile decision -n -t "Decision Title" -y "architectural" -p "high"
```

Interactive mode:
```bash
sigfile decision
```

View manual:
```bash
sigfile decision -man
```

List decisions:
```bash
sigfile decision list
```

### Development Environment Command

Manage permissions:
```bash
sigfile devenv permissions --role admin --permission write --on
```

View manual:
```bash
sigfile devenv -man
```

## Error Handling

The CLI provides comprehensive error handling:
- Validation errors for missing or invalid parameters
- File operation errors with helpful messages
- Permission errors with clear resolution steps
- Configuration errors with setup guidance

Error messages include:
- Error type and description
- Suggested resolution steps
- Command-specific context
- Reference to documentation

## Features

- Decision tracking with developer signatures
- Interactive and command-line modes
- Comprehensive manual pages
- Error handling with helpful messages
- Developer signature consistency enforcement
- Base command functionality for common operations
- Standardized file operations
- Metadata tracking and management

## Development

To contribute to the CLI:

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT License - see LICENSE file for details 