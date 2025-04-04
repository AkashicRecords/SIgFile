import os
import sys
from typing import Optional, Literal
import typer
from rich.console import Console
from rich.prompt import Prompt
from .utils.error_handling import handle_error
from .commands.decision import decision_command
from .commands.devenv import devenv_command

console = Console()
app = typer.Typer(help="SigFile CLI - Developer Signature Tracking")

@app.command()
def decision(
    new: bool = typer.Option(False, "--new", "-n", help="Create a new decision"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Decision title"),
    type: Optional[Literal["architectural", "implementation", "security", "performance", "user_experience"]] = typer.Option(None, "--type", "-y", help="Type of decision"),
    priority: Optional[Literal["high", "medium", "low"]] = typer.Option(None, "--priority", "-p", help="Priority of the decision"),
    manual: bool = typer.Option(False, "--manual", "-man", help="Show manual page")
):
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
            console.print("Try 'sigfile decision --help' for usage instructions")
            sys.exit(1)
            
        filepath = decision_command.create_decision(title, type, priority)
        console.print(f"\nDecision saved to: {filepath}")

@app.command()
def devenv(
    role: Optional[Literal["system", "ai_agent", "admin", "user", "all"]] = typer.Option(None, "--role", "-r", help="Role to modify"),
    permission: Optional[Literal["read", "write", "execute", "immutable"]] = typer.Option(None, "--permission", "-p", help="Permission to modify"),
    action: Optional[Literal["on", "off"]] = typer.Option(None, "--action", "-a", help="Action to take"),
    manual: bool = typer.Option(False, "--manual", "-man", help="Show manual page")
):
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
            console.print("Try 'sigfile devenv --help' for usage instructions")
            sys.exit(1)
            
        filepath = devenv_command.change_permission(role, permission, action)
        console.print(f"\nPermission change saved to: {filepath}")

def show_manual(command: str):
    """Show manual page for a command"""
    manual_path = os.path.join(os.path.dirname(__file__), "man", f"{command}.man")
    if os.path.exists(manual_path):
        with open(manual_path, "r") as f:
            console.print(f.read())
    else:
        console.print(f"[red]Manual page not found for command: {command}[/red]")

def main():
    app() 