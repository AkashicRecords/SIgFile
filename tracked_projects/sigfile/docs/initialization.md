# SigFile Project Initialization Guide

## Getting Started

### Installation and Setup

1. **Install the CLI Package**:
```zsh
pip install sigfile-cli
```

2. **Initialize a New Project**:
```zsh
sigfile init
```

3. **Setup an Existing Project**:
```zsh
sigfile setup
```

### Tracking a New Project

To start tracking a new project with SigFile:

1. **Initialize Project Tracking**:
```zsh
sigfile track-change --project "your-project-name" --type "documentation" --description "Initial project setup"
```

2. **Record Project Decisions**:
```zsh
sigfile decision -n -t "Title" -y architectural -p high
```
Or use interactive mode:
```zsh
sigfile decision
```

### Project Structure

After initialization, your project will have the following structure:

```
tracked_projects/
└── your-project-name/
    ├── changes/          # Daily change records and history
    ├── decisions/        # Project decisions and rationale
    ├── ai_conversations/ # AI interaction records
    ├── thinking/        # AI thinking process records
    └── handoffs/        # Handoff records between systems
```

### Important Notes

1. Always run commands from within the virtual environment
2. Use relative paths for all operations
3. All changes, decisions, and conversations are automatically tracked
4. Files are protected with immutable flags after creation
5. Commands must be run in zsh shell environment
6. Virtual environment activation should be done using:
```zsh
source venv/bin/activate
``` 