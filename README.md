# SigFile CLI

A command-line interface for the SigFile development process tracking tool.

## Project Information

**Identifier**: sigfile-cli  
**Version**: 1.0.0  
**Published**: 2024-04-03  
**Last Released**: 2024-04-03

## Description

SigFile CLI is the command-line interface component of the SigFile development process tracking tool. It provides a convenient way to interact with SigFile's core functionality through the terminal.

## Features

- Command-line interface for SigFile operations
- Development environment management
- Decision tracking and documentation
- Cross-platform support (Windows, macOS, Linux)

## Installation

1. Clone the repository:
   ```zsh
   git clone https://github.com/AkashicRecords/SigFile-CLI.git
   cd SigFile-CLI
   ```

2. Create and activate the virtual environment:
   ```zsh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package:
   ```zsh
   pip install -e .
   ```

## Usage

See the [User Guide](docs/user_guide.md) for detailed usage instructions.

Basic commands:
```zsh
# Track a decision
sigfile decision --project "my-project" --type "architecture" --description "Decision description"

# Manage development environment
sigfile devenv --action create --name "my-env"
```

## Documentation

- [User Guide](docs/user_guide.md)
- [Developer Guide](docs/developer_guide.md)
- [Architecture](docs/architecture.md)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
