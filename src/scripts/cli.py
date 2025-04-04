#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.scripts.track_change import (
    record_change, create_backup, show_history,
    setup, generate_handoff
)
from src.scripts.command_aliases import CommandAliases

def setup_cli():
    """Set up the command-line interface."""
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
                        print("God mode enabled: All permissions enabled for all roles")
                    elif args.off:
                        # Disable god mode (restore default permissions)
                        permission_manager.role_permissions = {
                            FileRole.SYSTEM: {
                                'read': True,
                                'write': True,
                                'execute': True,
                                'immutable': False
                            },
                            FileRole.AI_AGENT: {
                                'read': True,
                                'write': True,
                                'execute': True,
                                'immutable': False
                            },
                            FileRole.ADMIN: {
                                'read': True,
                                'write': True,
                                'execute': True,
                                'immutable': True
                            },
                            FileRole.USER: {
                                'read': True,
                                'write': False,
                                'execute': False,
                                'immutable': True
                            }
                        }
                        print("God mode disabled: Default permissions restored")
                
                elif args.venv:
                    if args.on:
                        permission_manager.enable_venv_restriction()
                        print("Venv restriction enabled: Files cannot be modified from within a virtual environment")
                    elif args.off:
                        permission_manager.disable_venv_restriction()
                        print("Venv restriction disabled: Files can be modified from within a virtual environment")
                
                elif args.role and args.permission:
                    if not args.on and not args.off:
                        print("Error: Must specify --on or --off when modifying role permissions")
                        return
                    
                    # Modify specific role permissions
                    role_map = {
                        'system': FileRole.SYSTEM,
                        'ai_agent': FileRole.AI_AGENT,
                        'admin': FileRole.ADMIN,
                        'user': FileRole.USER
                    }
                    
                    if args.role == 'all':
                        # Apply to all roles
                        for role in FileRole:
                            permission_manager.role_permissions[role][args.permission] = args.on
                        print(f"Permission '{args.permission}' {'enabled' if args.on else 'disabled'} for all roles")
                    else:
                        # Apply to specific role
                        role = role_map.get(args.role)
                        if role:
                            permission_manager.role_permissions[role][args.permission] = args.on
                            print(f"Permission '{args.permission}' {'enabled' if args.on else 'disabled'} for role '{args.role}'")
                        else:
                            print(f"Invalid role: {args.role}")
                
                else:
                    # Show current permissions
                    print("Current role permissions:")
                    for role, perms in permission_manager.role_permissions.items():
                        print(f"  {role.value}:")
                        for perm, value in perms.items():
                            print(f"    {perm}: {value}")
                    print("\nVenv restriction:", "enabled" if permission_manager.venv_restricted else "disabled")
        
        elif args.command == 'dev-mode':
            from src.scripts.track_change import OptimizedCapture
            
            # Create a capture instance
            capture = OptimizedCapture(args.project)
            
            if args.action == 'enable':
                capture.enable_dev_mode(args.file)
                print(f"Development mode {'enabled for all files' if args.file is None else f'enabled for {args.file}'}")
            else:
                capture.disable_dev_mode(args.file)
                print(f"Development mode {'disabled for all files' if args.file is None else f'disabled for {args.file}'}")
        
        elif args.command == 'decision':
            from src.scripts.track_change import OptimizedCapture
            capture = OptimizedCapture(args.project)
            
            if args.new:
                # Create new decision
                decision_type = args.type or "implementation"
                priority = args.priority or "medium"
                affected_files = args.affected_files or []
                
                if not args.title:
                    print("Error: Title is required for new decisions")
                    return
                
                capture._record_development_decision(
                    decision_type,
                    args.title,
                    args.context or "Context not provided",
                    "Pending",
                    affected_files
                )
                print(f"Created new decision: {args.title}")
                print(f"Type: {decision_type}")
                print(f"Priority: {priority}")
                if affected_files:
                    print("Affected files:")
                    for file in affected_files:
                        print(f"  - {file}")
            
            elif args.append:
                # Append to existing decision
                decision_id = args.append
                if not args.context:
                    print("Error: Context is required when appending to a decision")
                    return
                
                # TODO: Implement append to decision
                print(f"Appending to decision {decision_id}")
                print(f"New context: {args.context}")
            
            elif args.revert:
                # Revert a decision
                decision_id = args.revert
                if not args.context:
                    print("Error: Context is required when reverting a decision")
                    return
                
                # TODO: Implement decision revert
                print(f"Reverting decision {decision_id}")
                print(f"Revert reason: {args.context}")
            
            elif args.search:
                # Search for decisions
                search_term = args.search
                # TODO: Implement decision search
                print(f"Searching for decisions matching: {search_term}")
        
        elif args.command == 'record':
            record_change(args.description, ' '.join(args.files), args.project)
        
        elif args.command == 'backup':
            create_backup(args.file, args.project)
        
        elif args.command == 'history':
            show_history(args.date, args.project)
        
        elif args.command == 'setup':
            setup()
        
        elif args.command == 'handoff':
            generate_handoff(args.chat_name, args.chat_id, args.summary, args.next_steps, args.project)
        
        elif args.command == 'ai':
            if args.ai_command == 'start':
                # TODO: Implement AI session start
                pass
            elif args.ai_command == 'stop':
                # TODO: Implement AI session stop
                pass
            elif args.ai_command == 'history':
                # TODO: Implement AI session history
                pass
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 