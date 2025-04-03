# SigFile - AI Development Memory Keeper

SigFile is a Python-based tool designed to maintain a comprehensive record of your development process, including configuration changes, code modifications, and chat handoffs.

## Quick Links
- [Documentation Index](docs/README.md)
- [Installation Guide](docs/getting-started/installation.md)
- [Basic Usage](docs/getting-started/basic-usage.md)

## Version Compatibility
- Python: 3.8 or higher
- Operating Systems:
  - Windows 10/11
  - macOS 10.15+
  - Linux (Ubuntu 20.04+, RHEL 8+)

## Key Features
- 🤖 **AI Development Tracking**: Capture and document AI-assisted development changes
- 🔄 **Change Management**: Track and backup configuration changes
- 📝 **Change History**: Maintain detailed history with timestamps
- 📋 **Handoff Documentation**: Generate comprehensive handoff documents
- 📁 **Project-Specific Tracking**: Support for multiple projects
- 🌐 **Cross-Platform**: Works on any operating system

## Quick Start

1. **Install**:
```bash
git clone https://github.com/yourusername/sigfile.git
cd sigfile
pip install -r requirements.txt
```

2. **Setup**:
```bash
python src/scripts/track_change.py setup
```

3. **Basic Usage**:
```bash
# Record a change
python src/scripts/track_change.py record "description" "files_changed"

# View history
python src/scripts/track_change.py history

# Create backup
python src/scripts/track_change.py backup "path/to/file"
```

## Upcoming Features
- 🧪 **Unit Testing**: Comprehensive test suite for core functionality
- 🔍 **Enhanced AI Sessions**: Improved session tracking and analysis
- 📊 **Analytics Dashboard**: Visual representation of development patterns
- 🔄 **Real-time Change Detection**: Automatic change detection and recording
- 🔐 **Enhanced Security**: Improved handling of sensitive data
- 🔗 **Integration Capabilities**: Connect with other development tools
- 📝 **Git Integration**: Track commits, pushes, and branch changes automatically

## Next Steps
1. Test current release thoroughly
2. Fix any bugs or issues found
3. Implement unit testing framework
4. Enhance error handling and logging
5. Improve documentation coverage
6. Add basic security features

## Documentation
For detailed documentation, please visit our [Documentation Index](docs/README.md).

## Contributing
We welcome contributions! Please see our [Contributing Guide](docs/contributing/development.md) for details.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 