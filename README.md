# SigFile - Configuration Change Tracking System

SigFile is a tool designed to track and manage changes to development environments, with a focus on maintaining a clear history of modifications and enabling easy rollback capabilities.

## Project Structure

```
sigfile/
├── src/
│   └── scripts/
│       └── track_change.sh    # Main tracking script
├── tracked_projects/          # Projects being tracked
│   └── logiclens/            # LogicLens project tracking
│       ├── changes/          # Change logs
│       │   └── YYYYMMDD/     # Organized by date
│       ├── backups/          # File backups
│       │   └── YYYYMMDD/     # Organized by date
│       └── handoffs/         # Handoff documents
│           └── YYYYMMDD/     # Organized by date
└── [configuration files]
```

## Usage

The main script `track_change.sh` provides the following commands:

```bash
# Record a change
./src/scripts/track_change.sh record "description" "files_changed"

# Create a backup
./src/scripts/track_change.sh backup <file>

# Show change history
./src/scripts/track_change.sh history [YYYYMMDD]

# Generate handoff document
./src/scripts/track_change.sh handoff "chat_name" "chat_id" "summary" "next_steps"
```

## Current Status

This instance of SigFile is currently tracking changes to the LogicLens project. All changes are logged in the `tracked_projects/logiclens/` directory, organized by date.

## Dependencies

- moreutils (for timestamp functionality)
- zsh shell 