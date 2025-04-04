#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional
import subprocess

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.scripts.track_change import (
    record_change, create_backup, show_history,
    setup, generate_handoff
)
from src.scripts.command_aliases import CommandAliases
from src.scripts.cli_logging import cli_logger

def setup_cli():
    """Set up the command-line interface."""
    cli_logger.log_debug("Setting up CLI interface")
    
    parser = argparse.ArgumentParser(description='SigFile.ai - Change tracking and backup system')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # DevEnv command for development environment management
    devenv_parser = subparsers.add_parser('devenv', help='Manage development environment settings')
    devenv_subparsers = devenv_parser.add_subparsers(dest='devenv_command', help='Development environment commands')
    
    # Permissions subcommand
    permissions_parser = devenv_subparsers.add_parser('permissions', help='Manage development environment permissions')
    permissions_group = permissions_parser.add_mutually_exclusive_group(required=True)
    permissions_group.add_argument('--god-mode', action='store_true', help='Enable god mode (all permissions enabled)')
    permissions_group.add_argument('--venv', action='store_true', help='Enable/disable venv restriction')
    permissions_group.add_argument('--role', choices=['system', 'ai_agent', 'admin', 'user', 'all'], help='Role to modify permissions for')
    
    # Action group for permissions
    action_group = permissions_parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--on', action='store_true', help='Enable the specified permission')
    action_group.add_argument('--off', action='store_true', help='Disable the specified permission')
    
    # Permission type for role-specific changes
    permissions_parser.add_argument('--permission', choices=['read', 'write', 'execute', 'immutable'], 
                                  help='Permission to modify (required when using --role)')
    
    # Project argument
    permissions_parser.add_argument('--project', help='Project name')
    
    # DevMode command (keeping for backward compatibility)
    devmode_parser = subparsers.add_parser('dev-mode', help='Enable or disable development mode')
    devmode_parser.add_argument('action', choices=['enable', 'disable'], help='Action to perform')
    devmode_parser.add_argument('--file', help='File to enable/disable development mode for')
    devmode_parser.add_argument('--project', help='Project name')
    
    # Decision command
    decision_parser = subparsers.add_parser('decision', help='Record development decisions')
    decision_group = decision_parser.add_mutually_exclusive_group(required=True)
    decision_group.add_argument('-n', '--new', action='store_true', help='Create a new decision')
    decision_group.add_argument('-a', '--append', help='Append to an existing decision by ID')
    decision_group.add_argument('-r', '--revert', help='Revert a decision by ID')
    decision_group.add_argument('-s', '--search', help='Search for decisions by keyword')
    
    decision_parser.add_argument('-t', '--title', help='Decision title')
    decision_parser.add_argument('-c', '--context', help='Decision context')
    decision_parser.add_argument('--project', help='Project name')
    decision_parser.add_argument('--type', choices=['architectural', 'implementation', 'security', 'performance', 'user_experience'], 
                               help='Type of decision')
    decision_parser.add_argument('--priority', choices=['high', 'medium', 'low'], 
                               help='Priority of the decision')
    decision_parser.add_argument('--affected-files', nargs='+', help='Files affected by this decision')
    
    # Record command
    record_parser = subparsers.add_parser('record', help='Record a change')
    record_parser.add_argument('description', help='Description of the change')
    record_parser.add_argument('files', nargs='+', help='Files that were changed')
    record_parser.add_argument('--project', help='Project name')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create a backup of a file')
    backup_parser.add_argument('file', help='File to backup')
    backup_parser.add_argument('--project', help='Project name')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show change history')
    history_parser.add_argument('--date', help='Date to show history for (YYYYMMDD)')
    history_parser.add_argument('--project', help='Project name')
    
    # Handoff command
    handoff_parser = subparsers.add_parser('handoff', help='Generate a handoff document')
    handoff_parser.add_argument('chat_name', help='Name of the chat')
    handoff_parser.add_argument('chat_id', help='ID of the chat')
    handoff_parser.add_argument('summary', help='Summary of the conversation')
    handoff_parser.add_argument('next_steps', help='Next steps to take')
    handoff_parser.add_argument('--project', help='Project name')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Initialize SigFile')
    
    # AI command
    ai_parser = subparsers.add_parser('ai', help='AI-related commands')
    ai_subparsers = ai_parser.add_subparsers(dest='ai_command', help='AI commands')
    
    # AI start command
    ai_start_parser = ai_subparsers.add_parser('start', help='Start an AI session')
    ai_start_parser.add_argument('--project', help='Project name')
    
    # AI stop command
    ai_stop_parser = ai_subparsers.add_parser('stop', help='Stop an AI session')
    ai_stop_parser.add_argument('--project', help='Project name')
    
    # AI history command
    ai_history_parser = ai_subparsers.add_parser('history', help='Show AI session history')
    ai_history_parser.add_argument('--project', help='Project name')
    
    return parser

def show_man_page():
    """Show the man page for the CLI tool."""
    try:
        man_path = os.path.join(os.path.dirname(__file__), 'man', 'sigfile-cli.1')
        if os.path.exists(man_path):
            subprocess.run(['man', man_path], check=True)
        else:
            print("Man page not found. Please check the documentation.")
    except subprocess.CalledProcessError:
        print("Error displaying man page. Please check the documentation.")

def main():
    """Main entry point for the CLI."""
    parser = setup_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Set default project if not provided
    if not hasattr(args, 'project') or args.project is None:
        args.project = 'sigfile'  # Default project name
    
    try:
        # Log command execution
        cli_logger.log_command(args.command, vars(args))
        
        if args.command == 'devenv':
            from src.scripts.permission_manager import permission_manager, FileRole
            from src.scripts.track_change import OptimizedCapture
            
            # Create a capture instance for recording decisions
            capture = OptimizedCapture(args.project)
            
            if args.devenv_command == 'permissions':
                if args.god_mode:
                    if args.on:
                        # Enable god mode (all permissions enabled for all roles)
                        for role in FileRole:
                            for perm in ['read', 'write', 'execute', 'immutable']:
                                permission_manager.role_permissions[role][perm] = True
                        cli_logger.log_success("God mode enabled: All permissions enabled for all roles")
                    else:
                        # Disable god mode
                        for role in FileRole:
                            for perm in ['read', 'write', 'execute', 'immutable']:
                                permission_manager.role_permissions[role][perm] = False
                        cli_logger.log_success("God mode disabled: All permissions reset to default")
        
        elif args.command == 'dev-mode':
            from src.scripts.track_change import OptimizedCapture
            
            # Create a capture instance
            capture = OptimizedCapture(args.project)
            
            if args.action == 'enable':
                capture.enable_dev_mode(args.file)
                cli_logger.log_success(f"Development mode {'enabled for all files' if args.file is None else f'enabled for {args.file}'}")
            else:
                capture.disable_dev_mode(args.file)
                cli_logger.log_success(f"Development mode {'disabled for all files' if args.file is None else f'disabled for {args.file}'}")
        
        elif args.command == 'decision':
            from src.scripts.track_change import OptimizedCapture
            capture = OptimizedCapture(args.project)
            
            if args.new:
                # Create new decision
                decision_type = args.type or "implementation"
                priority = args.priority or "medium"
                affected_files = args.affected_files or []
                
                if not args.title:
                    cli_logger.log_error(ValueError("Title is required for new decisions"))
                    return
                
                capture._record_development_decision(
                    decision_type,
                    args.title,
                    args.context or "Context not provided",
                    "Pending",
                    affected_files
                )
                cli_logger.log_success(f"Created new decision: {args.title}")
                cli_logger.log_debug(f"Type: {decision_type}")
                cli_logger.log_debug(f"Priority: {priority}")
                if affected_files:
                    cli_logger.log_debug("Affected files:")
                    for file in affected_files:
                        cli_logger.log_debug(f"  - {file}")
        
        elif args.command == 'record':
            record_change(args.description, ' '.join(args.files), args.project)
            cli_logger.log_success(f"Recorded change: {args.description}")
        
        elif args.command == 'backup':
            create_backup(args.file, args.project)
            cli_logger.log_success(f"Created backup for: {args.file}")
        
        elif args.command == 'history':
            show_history(args.date, args.project)
            cli_logger.log_debug(f"Showed history for date: {args.date or 'today'}")
        
        elif args.command == 'setup':
            setup()
            cli_logger.log_success("SigFile setup completed")
        
        elif args.command == 'handoff':
            generate_handoff(args.chat_name, args.chat_id, args.summary, args.next_steps, args.project)
            cli_logger.log_success(f"Generated handoff for chat: {args.chat_name}")
        
        elif args.command == 'ai':
            if args.ai_command == 'start':
                # TODO: Implement AI session start
                cli_logger.log_warning("AI session start not yet implemented")
            elif args.ai_command == 'stop':
                # TODO: Implement AI session stop
                cli_logger.log_warning("AI session stop not yet implemented")
            elif args.ai_command == 'history':
                # TODO: Implement AI session history
                cli_logger.log_warning("AI session history not yet implemented")
    
    except Exception as e:
        cli_logger.log_error(e, f"Error executing command: {args.command}")
        print(f"\nError: {e}")
        print("\nFor correct usage, please check the man page:")
        show_man_page()
        sys.exit(1)

if __name__ == '__main__':
    main() 