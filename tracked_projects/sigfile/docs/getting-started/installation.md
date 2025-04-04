# Installation Guide

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Git (for version control)
- Operating System:
  - Windows 10/11
  - macOS 10.15+
  - Linux (Ubuntu 20.04+, RHEL 8+)

## Installation Steps

### 1. Install the CLI Package
```bash
pip install sigfile-cli
```

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/sigfile.git
cd sigfile
```

### 3. Install Development Dependencies
```bash
pip install -e .
```

### 4. Initialize the Project
```bash
sigfile init
```

### 5. Set Up Development Environment
```bash
sigfile setup
```

## Verification
To verify your installation:
```bash
# Check CLI version
sigfile --version

# Verify command availability
sigfile decision --help
sigfile dev --help
sigfile handoff --help
```

## Dependencies
The CLI package depends on:
- click (for command-line interface)
- rich (for terminal formatting)
- gitpython (for developer ID detection)

## Troubleshooting
If you encounter any issues during installation:
1. Ensure Python 3.7+ is installed and in your PATH
2. Check pip is up to date: `pip install --upgrade pip`
3. Verify virtual environment setup if using one
4. Check network connectivity for package downloads
5. Verify all dependencies are installed correctly

## Platform-Specific Notes
### Windows
- Ensure Python is added to PATH during installation
- Use PowerShell or Command Prompt with administrator privileges if needed

### macOS
- Consider using Homebrew for Python installation
- Ensure Xcode Command Line Tools are installed

### Linux
- Use system package manager for Python installation
- Ensure build essentials are installed

## Next Steps
After installation, proceed to the [Basic Usage](basic-usage.md) guide to start using SigFile. 