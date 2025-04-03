# Installation Guide

This guide covers the installation process for SigFile across different platforms and environments.

## System Requirements

- Python 3.8 or higher
- Operating System:
  - Windows 10/11
  - macOS 10.15+
  - Linux (Ubuntu 20.04+, RHEL 8+)
- Git (for version control integration)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sigfile.git
cd sigfile
```

### 2. Create a Virtual Environment (Recommended)

#### Windows
```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize SigFile

```bash
python src/scripts/track_change.py setup
```

## Platform-Specific Setup

### Windows

1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Install Git from [git-scm.com](https://git-scm.com/download/win)
3. Follow the general installation steps above

### macOS

1. Install Python using Homebrew:
```bash
brew install python@3.8
```

2. Install Git:
```bash
brew install git
```

3. Follow the general installation steps above

### Linux (Ubuntu)

1. Install Python and Git:
```bash
sudo apt update
sudo apt install python3.8 python3.8-venv git
```

2. Follow the general installation steps above

## Verification

To verify your installation, run:

```bash
python src/scripts/track_change.py --version
```

## Troubleshooting

Common installation issues and solutions:

1. **Python Version Issues**
   - Ensure Python 3.8+ is installed
   - Check with `python --version`

2. **Dependencies Issues**
   - Try updating pip: `pip install --upgrade pip`
   - Install build tools: `pip install wheel setuptools`

3. **Permission Issues**
   - Use `sudo` on Linux/macOS if needed
   - Run as administrator on Windows

For more help, see the [Troubleshooting Guide](../troubleshooting/common-issues.md). 