# Basic Usage Guide

This guide covers the basic usage of SigFile, including file tracking, backups, and AI session management.

## File Tracking

### Recording Changes
```bash
python src/scripts/track_change.py record "description" "files_changed"
```

Example:
```bash
python src/scripts/track_change.py record "Updated user authentication" "src/auth/login.py src/auth/register.py"
```

### Viewing History
```bash
# View all changes
python src/scripts/track_change.py history

# View changes for a specific date
python src/scripts/track_change.py history 20240302
```

## Backup Management

### Creating Backups
```bash
python src/scripts/track_change.py backup "path/to/file"
```

Example:
```bash
python src/scripts/track_change.py backup "config/settings.json"
```

### Restoring Backups
```bash
python src/scripts/track_change.py restore "path/to/backup"
```

## AI Session Management

### Starting an AI Session
```bash
python src/scripts/track_change.py ai-record "session-name" "Description of what you're working on"
```

Example:
```bash
python src/scripts/track_change.py ai-record "feature-implementation" "Implementing new user dashboard with AI assistance"
```

### AI Session Storage
AI sessions are stored in the following structure:
```
tracked_projects/
└── <project_name>/
    └── ai_conversations/
        └── conversation_<session-name>_<timestamp>.json
```

Each session file contains:
- Chat ID and project name
- Timestamp and date
- Messages exchanged
- Code changes made
- Summary and key decisions
- Impact areas and next steps

### During an AI Session
- All changes made during the session are automatically linked to the session
- Use regular record commands to track specific changes
- The AI session provides context for all changes made
- Session data is stored in JSON format for easy access and analysis

### Best Practices
1. Start a new AI session for each distinct task or feature
2. Provide clear, descriptive session names
3. Include relevant context in the session description
4. Record significant changes during the session
5. Review session JSON files for complete conversation history

## Project-Specific Usage

### Setting Project Context
```bash
python src/scripts/track_change.py -p project_name <command>
```

Example:
```bash
python src/scripts/track_change.py -p webapp record "Updated API endpoints" "src/api/*.py"
```

## Common Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `record` | Record a change | `record "Updated UI" "src/ui/*"` |
| `backup` | Create a backup | `backup "config.json"` |
| `history` | View change history | `history 20240302` |
| `ai-record` | Start AI session | `ai-record "feature" "description"` |

## Next Steps
- Learn about [Advanced Usage](../advanced/)
- Explore [AI Development Features](../features/ai-tracking.md)
- Check out [Project Organization](../features/project-organization.md) 