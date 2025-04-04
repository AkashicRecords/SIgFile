#!/bin/zsh

# Configuration change tracking script for SigFile
# This script helps track and manage changes to development environments

# Configuration
SIGFILE_DIR="$(pwd)"
PROJECT_NAME="logiclens"  # Default project, can be overridden with -p flag
CONFIG_DIR="$SIGFILE_DIR/tracked_projects/$PROJECT_NAME"
CHANGES_DIR="$CONFIG_DIR/changes"
BACKUPS_DIR="$CONFIG_DIR/backups"
HANDOFF_DIR="$CONFIG_DIR/handoffs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE_DIR=$(date +%Y%m%d)

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to log messages with timestamps
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | ts '[%Y-%m-%d %H:%M:%S]'
}

# Function to create backup
create_backup() {
    local file=$1
    local backup_name=$2
    
    if [ -f "$file" ]; then
        mkdir -p "$BACKUPS_DIR/$DATE_DIR"
        cp "$file" "$BACKUPS_DIR/$DATE_DIR/$backup_name.$TIMESTAMP"
        log "Created backup: $backup_name.$TIMESTAMP"
    else
        log "No file to backup: $file"
    fi
}

# Function to record change
record_change() {
    local description=$1
    local files_changed=$2
    
    mkdir -p "$CHANGES_DIR/$DATE_DIR"
    local change_log="$CHANGES_DIR/$DATE_DIR/changes_$TIMESTAMP.md"
    
    {
        echo "# Change Record - $(date '+%Y-%m-%d %H:%M:%S')"
        echo
        echo "## Description"
        echo "$description"
        echo
        echo "## Files Changed"
        echo "$files_changed"
        echo
        echo "## Timestamp"
        echo "$TIMESTAMP"
    } > "$change_log"
    
    log "Recorded change in: $change_log"
}

# Function to show change history
show_history() {
    local date=$1
    if [ -z "$date" ]; then
        date=$(date +%Y%m%d)
    fi
    
    if [ -d "$CHANGES_DIR/$date" ]; then
        log "Changes for $date:"
        for change in "$CHANGES_DIR/$date"/changes_*.md; do
            if [ -f "$change" ]; then
                echo "---"
                cat "$change"
            fi
        done
    else
        log "No changes recorded for $date"
    fi
}

# Function to generate chat handoff document
generate_handoff() {
    local chat_name=$1
    local chat_id=$2
    local summary=$3
    local next_steps=$4
    
    mkdir -p "$HANDOFF_DIR/$DATE_DIR"
    local handoff_file="$HANDOFF_DIR/$DATE_DIR/handoff_${chat_name}_${TIMESTAMP}.md"
    
    {
        echo "# Chat Handoff Document - $chat_name"
        echo
        echo "## Chat Information"
        echo "- Chat ID: $chat_id"
        echo "- Date: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "- Timestamp: $TIMESTAMP"
        echo
        echo "## Summary"
        echo "$summary"
        echo
        echo "## Next Steps"
        echo "$next_steps"
        echo
        echo "## Related Changes"
        echo "Recent changes in this chat:"
        if [ -d "$CHANGES_DIR/$DATE_DIR" ]; then
            for change in "$CHANGES_DIR/$DATE_DIR"/changes_*.md; do
                if [ -f "$change" ]; then
                    echo "---"
                    cat "$change"
                fi
            done
        else
            echo "No changes recorded for today"
        fi
        echo
        echo "## Configuration State"
        echo "Current configuration backups:"
        if [ -d "$BACKUPS_DIR/$DATE_DIR" ]; then
            ls -l "$BACKUPS_DIR/$DATE_DIR"
        else
            echo "No backups for today"
        fi
    } > "$handoff_file"
    
    log "Generated handoff document: $handoff_file"
}

# Function to setup SigFile
setup() {
    # Check for moreutils
    if ! command_exists ts; then
        log "Installing moreutils..."
        if command_exists brew; then
            brew install moreutils
        else
            log "ERROR: Homebrew not found. Please install moreutils manually."
            exit 1
        fi
    fi
    
    # Create directory structure
    mkdir -p "$SIGFILE_DIR"/{config/{settings,backups,changes,handoffs},src/{scripts,templates}}
    
    # Set permissions
    chmod +x "$0"
    
    log "SigFile setup complete!"
}

# Main script
while getopts "p:" opt; do
    case $opt in
        p) PROJECT_NAME="$OPTARG";;
        \?) echo "Invalid option -$OPTARG" >&2; exit 1;;
    esac
done

# Update config directory based on project
CONFIG_DIR="$SIGFILE_DIR/tracked_projects/$PROJECT_NAME"
CHANGES_DIR="$CONFIG_DIR/changes"
BACKUPS_DIR="$CONFIG_DIR/backups"
HANDOFF_DIR="$CONFIG_DIR/handoffs"

case "${@:$OPTIND:1}" in
    "backup")
        if [ -z "${@:$OPTIND+1:1}" ]; then
            log "ERROR: Please provide a file to backup"
            echo "Usage: $0 [-p project_name] backup <file>"
            exit 1
        fi
        create_backup "${@:$OPTIND+1:1}" "$(basename "${@:$OPTIND+1:1}")"
        ;;
    "record")
        if [ -z "${@:$OPTIND+1:1}" ] || [ -z "${@:$OPTIND+2:1}" ]; then
            log "ERROR: Please provide description and files changed"
            echo "Usage: $0 [-p project_name] record \"description\" \"files_changed\""
            exit 1
        fi
        record_change "${@:$OPTIND+1:1}" "${@:$OPTIND+2:1}"
        ;;
    "history")
        show_history "${@:$OPTIND+1:1}"
        ;;
    "handoff")
        if [ -z "${@:$OPTIND+1:1}" ] || [ -z "${@:$OPTIND+2:1}" ] || [ -z "${@:$OPTIND+3:1}" ] || [ -z "${@:$OPTIND+4:1}" ]; then
            log "ERROR: Please provide all required handoff information"
            echo "Usage: $0 [-p project_name] handoff \"chat_name\" \"chat_id\" \"summary\" \"next_steps\""
            exit 1
        fi
        generate_handoff "${@:$OPTIND+1:1}" "${@:$OPTIND+2:1}" "${@:$OPTIND+3:1}" "${@:$OPTIND+4:1}"
        ;;
    "setup")
        setup
        ;;
    *)
        echo "Usage:"
        echo "  $0 [-p project_name] setup                    # Initialize SigFile"
        echo "  $0 [-p project_name] backup <file>           # Create backup of a file"
        echo "  $0 [-p project_name] record \"description\" \"files\"    # Record a change"
        echo "  $0 [-p project_name] history [YYYYMMDD]      # Show change history"
        echo "  $0 [-p project_name] handoff \"chat_name\" \"chat_id\" \"summary\" \"next_steps\"  # Generate handoff document"
        exit 1
        ;;
esac 