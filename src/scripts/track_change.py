#!/usr/bin/env python3

import os
import sys
import argparse
import datetime
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import json

# Import AI tracking modules
from ai_tracking import AITracking
from decision_tracking import DecisionTracker

# Configuration
SIGFILE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_NAME = "logiclens"  # Default project, can be overridden with -p flag

def get_config_dirs(project_name):
    """Get configuration directories for the specified project."""
    config_dir = os.path.join(SIGFILE_DIR, "tracked_projects", project_name)
    return {
        'config': config_dir,
        'changes': os.path.join(config_dir, "changes"),
        'backups': os.path.join(config_dir, "backups"),
        'handoffs': os.path.join(config_dir, "handoffs")
    }

def get_timestamp():
    """Get current timestamp in required format."""
    now = datetime.datetime.now()
    return {
        'timestamp': now.strftime("%Y%m%d_%H%M%S"),
        'date': now.strftime("%Y%m%d")
    }

def log(message):
    """Log message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_backup(file_path, project_name):
    """Create a backup of the specified file."""
    if not os.path.exists(file_path):
        log(f"No file to backup: {file_path}")
        return

    dirs = get_config_dirs(project_name)
    timestamps = get_timestamp()
    backup_dir = os.path.join(dirs['backups'], timestamps['date'])
    os.makedirs(backup_dir, exist_ok=True)

    backup_name = f"{os.path.basename(file_path)}_{timestamps['timestamp']}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    try:
        subprocess.run(['cp', file_path, backup_path], check=True)
        log(f"Created backup: {backup_name}")
    except subprocess.CalledProcessError as e:
        log(f"Error creating backup: {e}")

def record_change(description, files_changed, project_name):
    """Record a change with description and files changed."""
    dirs = get_config_dirs(project_name)
    timestamps = get_timestamp()
    changes_dir = os.path.join(dirs['changes'], timestamps['date'])
    os.makedirs(changes_dir, exist_ok=True)

    change_log = os.path.join(changes_dir, f"changes_{timestamps['timestamp']}.md")
    
    with open(change_log, 'w') as f:
        f.write(f"# Change Record - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Description\n")
        f.write(f"{description}\n\n")
        f.write("## Files Changed\n")
        f.write(f"{files_changed}\n\n")
        f.write("## Timestamp\n")
        f.write(f"{timestamps['timestamp']}\n")
    
    log(f"Recorded change in: {change_log}")

def show_history(date, project_name):
    """Show change history for the specified date."""
    if not date:
        date = datetime.datetime.now().strftime("%Y%m%d")
    
    dirs = get_config_dirs(project_name)
    changes_dir = os.path.join(dirs['changes'], date)
    
    if not os.path.exists(changes_dir):
        log(f"No changes recorded for {date}")
        return
    
    for change_file in sorted(Path(changes_dir).glob("changes_*.md")):
        print("---")
        with open(change_file, 'r') as f:
            print(f.read())

def generate_handoff(chat_name, chat_id, summary, next_steps, project_name):
    """Generate a handoff document."""
    dirs = get_config_dirs(project_name)
    timestamps = get_timestamp()
    handoff_dir = os.path.join(dirs['handoffs'], timestamps['date'])
    os.makedirs(handoff_dir, exist_ok=True)

    handoff_file = os.path.join(handoff_dir, f"handoff_{chat_name}_{timestamps['timestamp']}.md")
    
    with open(handoff_file, 'w') as f:
        f.write(f"# Chat Handoff Document - {chat_name}\n\n")
        f.write("## Chat Information\n")
        f.write(f"- Chat ID: {chat_id}\n")
        f.write(f"- Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- Timestamp: {timestamps['timestamp']}\n\n")
        f.write("## Summary\n")
        f.write(f"{summary}\n\n")
        f.write("## Next Steps\n")
        f.write(f"{next_steps}\n\n")
        f.write("## Related Changes\n")
        f.write("Recent changes in this chat:\n")
        
        changes_dir = os.path.join(dirs['changes'], timestamps['date'])
        if os.path.exists(changes_dir):
            for change_file in sorted(Path(changes_dir).glob("changes_*.md")):
                f.write("---\n")
                with open(change_file, 'r') as cf:
                    f.write(cf.read())
        else:
            f.write("No changes recorded for today\n")
        
        f.write("\n## Configuration State\n")
        f.write("Current configuration backups:\n")
        backup_dir = os.path.join(dirs['backups'], timestamps['date'])
        if os.path.exists(backup_dir):
            for backup in os.listdir(backup_dir):
                f.write(f"- {backup}\n")
        else:
            f.write("No backups for today\n")
    
    log(f"Generated handoff document: {handoff_file}")

def setup():
    """Set up SigFile environment."""
    # Check for moreutils
    try:
        subprocess.run(['ts', '--version'], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        log("Installing moreutils...")
        try:
            subprocess.run(['brew', 'install', 'moreutils'], check=True)
        except subprocess.CalledProcessError:
            log("ERROR: Homebrew not found. Please install moreutils manually.")
            sys.exit(1)
    
    # Create directory structure
    for dir_name in ['config/settings', 'config/backups', 'config/changes', 'config/handoffs', 'src/scripts', 'src/templates']:
        os.makedirs(os.path.join(SIGFILE_DIR, dir_name), exist_ok=True)
    
    log("SigFile setup complete!")

def main():
    parser = argparse.ArgumentParser(description='SigFile - AI Development Memory Keeper')
    parser.add_argument('-p', '--project', default=PROJECT_NAME, help='Project name')
    parser.add_argument('command', choices=['backup', 'record', 'history', 'handoff', 'setup', 'version',
                                          'ai-record', 'ai-dataset', 'ai-analyze',
                                          'decision-record', 'decision-analyze'],
                       help='Command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')
    
    args = parser.parse_args()
    
    if args.command == 'version':
        print("SigFile v1.0.0")
        return
    
    if args.command == 'setup':
        setup()
        return
    
    if args.command == 'backup':
        if not args.args:
            log("ERROR: Please provide a file to backup")
            print("Usage: sigfile [-p project_name] backup <file>")
            sys.exit(1)
        create_backup(args.args[0], args.project)
    
    elif args.command == 'record':
        if len(args.args) < 2:
            log("ERROR: Please provide description and files changed")
            print("Usage: sigfile [-p project_name] record \"description\" \"files_changed\"")
            sys.exit(1)
        record_change(args.args[0], args.args[1], args.project)
    
    elif args.command == 'history':
        show_history(args.args[0] if args.args else None, args.project)
    
    elif args.command == 'handoff':
        if len(args.args) < 4:
            log("ERROR: Please provide all required handoff information")
            print("Usage: sigfile [-p project_name] handoff \"chat_name\" \"chat_id\" \"summary\" \"next_steps\"")
            sys.exit(1)
        generate_handoff(args.args[0], args.args[1], args.args[2], args.args[3], args.project)
    
    # AI Tracking Commands
    elif args.command == 'ai-record':
        if not args.args:
            log("ERROR: Please provide chat ID")
            print("Usage: sigfile [-p project_name] ai-record <chat_id>")
            sys.exit(1)
        ai_tracker = AITracking(args.project)
        # Example conversation data
        messages = [
            {"role": "user", "content": "How do I implement feature X?"},
            {"role": "assistant", "content": "Here's how to implement feature X..."}
        ]
        code_changes = [
            {"file": "src/feature.py", "type": "add", "content": "def new_feature():\n    pass"}
        ]
        ai_tracker.record_conversation(args.args[0], messages, code_changes)
    
    elif args.command == 'ai-dataset':
        ai_tracker = AITracking(args.project)
        format = args.args[0] if args.args else "jsonl"
        include_code = "--include-code" in args.args
        ai_tracker.generate_dataset(format, include_code)
    
    elif args.command == 'ai-analyze':
        ai_tracker = AITracking(args.project)
        ai_tracker.analyze_conversations()
    
    # Decision Tracking Commands
    elif args.command == 'decision-record':
        if len(args.args) < 5:
            log("ERROR: Please provide all required decision information")
            print("Usage: sigfile [-p project_name] decision-record <decision_id> <description> <rationale> <alternatives_json> <impact_json> [code_changes_json]")
            sys.exit(1)
        decision_tracker = DecisionTracker(args.project)
        decision_tracker.record_decision(
            args.args[0],  # decision_id
            args.args[1],  # description
            args.args[2],  # rationale
            json.loads(args.args[3]),  # alternatives
            json.loads(args.args[4]),  # impact
            json.loads(args.args[5]) if len(args.args) > 5 else None  # code_changes
        )
    
    elif args.command == 'decision-analyze':
        decision_tracker = DecisionTracker(args.project)
        decision_tracker.analyze_decisions()

if __name__ == '__main__':
    main() 