import os
import sys
import click
from rich.console import Console
from rich.prompt import Prompt
from .utils.error_handling import handle_error
from .commands.decision import decision_command
from .commands.devenv import devenv_command

console = Console()

@click.group()
def cli():
    """SigFile CLI - Developer Signature Tracking"""
    pass

@cli.command()
@click.option('-n', '--new', is_flag=True, help='Create a new decision')
@click.option('-t', '--title', help='Decision title')
@click.option('-y', '--type', type=click.Choice(['architectural', 'implementation', 'security', 'performance', 'user_experience']), help='Type of decision')
@click.option('-p', '--priority', type=click.Choice(['high', 'medium', 'low']), help='Priority of the decision')
@click.option('-man', '--manual', is_flag=True, help='Show manual page')
@handle_error
def decision(new, title, type, priority, manual):
    """Manage development decisions"""
    if manual:
        show_manual('decision')
        return

    if not any([new, title, type, priority]):
        # Interactive mode
        try:
            console.print("\n[bold]Creating New Decision[/bold]")
            console.print("Press Ctrl+C at any time to cancel\n")
            
            title = Prompt.ask("Decision title")
            type = Prompt.ask("Decision type", choices=['architectural', 'implementation', 'security', 'performance', 'user_experience'])
            priority = Prompt.ask("Priority", choices=['high', 'medium', 'low'])
            
            # Show final command
            console.print("\n[bold]Final Command:[/bold]")
            console.print(f"sigfile decision -n -t \"{title}\" -y {type} -p {priority}")
            
            if Prompt.ask("\nExecute command?", choices=['y', 'n'], default='y') == 'y':
                filepath = decision_command.create_decision(title, type, priority)
                console.print(f"\nDecision saved to: {filepath}")
            else:
                console.print("Operation cancelled")
                
        except KeyboardInterrupt:
            console.print("\nOperation cancelled by user")
            sys.exit(0)
    else:
        # Command line mode
        if not all([new, title, type, priority]):
            console.print("[red]Error: All options are required in command line mode[/red]")
            console.print("Try 'sigfile decision -man' for usage instructions")
            sys.exit(1)
            
        filepath = decision_command.create_decision(title, type, priority)
        console.print(f"\nDecision saved to: {filepath}")

@cli.command()
@click.option('-r', '--role', type=click.Choice(['system', 'ai_agent', 'admin', 'user', 'all']), help='Role to modify')
@click.option('-p', '--permission', type=click.Choice(['read', 'write', 'execute', 'immutable']), help='Permission to modify')
@click.option('-a', '--action', type=click.Choice(['on', 'off']), help='Action to take')
@click.option('-man', '--manual', is_flag=True, help='Show manual page')
@handle_error
def devenv(role, permission, action, manual):
    """Manage development environment"""
    if manual:
        show_manual('devenv')
        return

    if not any([role, permission, action]):
        # Interactive mode
        try:
            console.print("\n[bold]Modifying Development Environment[/bold]")
            console.print("Press Ctrl+C at any time to cancel\n")
            
            role = Prompt.ask("Role", choices=['system', 'ai_agent', 'admin', 'user', 'all'])
            permission = Prompt.ask("Permission", choices=['read', 'write', 'execute', 'immutable'])
            action = Prompt.ask("Action", choices=['on', 'off'])
            
            # Show final command
            console.print("\n[bold]Final Command:[/bold]")
            console.print(f"sigfile devenv -r {role} -p {permission} -a {action}")
            
            if Prompt.ask("\nExecute command?", choices=['y', 'n'], default='y') == 'y':
                filepath = devenv_command.change_permission(role, permission, action)
                console.print(f"\nPermission change saved to: {filepath}")
            else:
                console.print("Operation cancelled")
                
        except KeyboardInterrupt:
            console.print("\nOperation cancelled by user")
            sys.exit(0)
    else:
        # Command line mode
        if not all([role, permission, action]):
            console.print("[red]Error: All options are required in command line mode[/red]")
            console.print("Try 'sigfile devenv -man' for usage instructions")
            sys.exit(1)
            
        filepath = devenv_command.change_permission(role, permission, action)
        console.print(f"\nPermission change saved to: {filepath}")

def show_manual(command):
    """Display manual page for a command"""
    manual_path = os.path.join(os.path.dirname(__file__), 'man', f'{command}.man')
    try:
        with open(manual_path, 'r') as f:
            console.print(f.read())
    except FileNotFoundError:
        console.print(f"[red]Manual page for {command} not found[/red]")

def main():
    """Main entry point"""
    cli() 