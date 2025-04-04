# SigFile - AI Development Memory Keeper

> "In the digital age, your development history is your most valuable asset. SigFile helps you preserve it."

## Documentation Formats
- [HTML Version](README.html) - Marketplace-style documentation
- [Technical Specification](README.txt) - Detailed technical documentation
- [Markdown Version](README.md) - This file

## Project Information
- **Identifier**: sigfile.ai-dev-memory
- **Version**: 1.0.0
- **Status**: Active
- **Last Updated**: 2024-04-03

## Quick Links
- [Installation Guide](getting-started/installation.md)
- [Basic Usage](getting-started/basic-usage.md)
- [API Documentation](api/README.md)
- [Contributing Guide](contributing/README.md)

## Features
- 🤖 **AI Development Tracking**: Capture and document AI-assisted development changes
- 🔄 **Change Management**: Track and backup configuration changes
- 📝 **Change History**: Maintain detailed history with timestamps
- 📋 **Handoff Documentation**: Generate comprehensive handoff documents
- 📁 **Project-Specific Tracking**: Support for multiple projects
- 🌐 **Cross-Platform**: Works on any operating system
- 🔐 **Role-Based Permissions**: Granular control over file access and modifications
- 📊 **Decision Tracking**: Record and track development decisions

## Quick Start

1. **Install**:
```bash
# Install the CLI package
pip install sigfile-cli

# Or install from source
git clone https://github.com/yourusername/sigfile.git
cd sigfile
pip install -e .
```

2. **Setup**:
```bash
# Initialize a new project
sigfile init

# Or setup an existing project
sigfile setup
```

3. **Basic Usage**:
```bash
# Record a decision
sigfile decision -n -t "Decision Title" -y "architectural" -p "high"

# View decision history
sigfile decision list

# Manage development environment
sigfile devenv permissions --role admin --permission write --on

# Create a handoff document
sigfile handoff create "Handoff Title" "Description"
```

## Documentation Structure
- [Advanced Features](advanced/README.md)
- [API Reference](api/README.md)
- [Platform Guides](platforms/README.md)
- [Troubleshooting](troubleshooting/README.md)
- [Feature Documentation](features/README.md)

## Development Status
- Core functionality: Complete
- Testing: In Progress
- Documentation: In Progress
- Security: In Progress

## Contributing
We welcome contributions! Please see our [Contributing Guide](contributing/README.md) for details.

## License
This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details. 