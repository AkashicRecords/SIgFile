# Quick Start Guide

This guide will help you get started with SigFile quickly. For detailed information, please refer to the [Installation Guide](installation.md) and [Basic Usage](basic-usage.md).

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sigfile.git
cd sigfile
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize SigFile:
```bash
python src/scripts/track_change.py setup
```

## Basic Usage

### 1. Record Changes
```bash
python src/scripts/track_change.py record "Updated user interface" "src/ui/main.py"
```

### 2. Create Backups
```bash
python src/scripts/track_change.py backup "config/settings.json"
```

### 3. View History
```bash
python src/scripts/track_change.py history
```

### 4. Track AI Sessions
```bash
# Start a new AI session
python src/scripts/track_change.py ai-record "session-name" "Description of what you're working on"

# Record changes during the AI session
python src/scripts/track_change.py record "Made changes with AI assistance" "files_changed"

# View AI session data
# AI sessions are stored in tracked_projects/<project_name>/ai_conversations/
# Each session is saved as a JSON file with format: conversation_<session-name>_<timestamp>.json
```

## Next Steps

- Learn about [Basic Usage](basic-usage.md)
- Explore [AI Development Tracking](../features/ai-tracking.md)
- Check out [Project Organization](../features/project-organization.md)
- View [Platform-Specific Guides](../platforms/) 