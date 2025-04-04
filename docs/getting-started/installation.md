# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

## Installation Steps

1. Clone the repository:
```zsh
git clone https://github.com/yourusername/sigfile.git
cd sigfile
```

2. Create and activate a virtual environment:

#### Windows
```powershell
python -m venv Sigfile
.\Sigfile\Scripts\activate
```

#### macOS/Linux
```zsh
python3 -m venv Sigfile
source Sigfile/bin/activate
```

3. Install dependencies:
```zsh
pip install -r requirements.txt
```

4. Verify the installation:
```zsh
python src/scripts/track_change.py --version
```

## Troubleshooting

If you encounter any issues during installation, please refer to the [Troubleshooting Guide](../troubleshooting/common-issues.md).

## Next Steps

After successful installation, you can:
- Configure your development environment
- Start tracking changes in your projects
- Review the [User Guide](../user-guide/README.md) for detailed usage instructions 