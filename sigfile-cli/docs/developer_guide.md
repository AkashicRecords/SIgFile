# SigFile CLI Developer Guide

## Introduction

This guide explains how to extend the SigFile CLI with new commands and functionality. The CLI is designed to be easily extensible while maintaining a consistent user experience.

## Architecture Overview

The CLI follows a modular architecture with these key components:

1. **BaseCommand Class**: Provides common functionality for all commands
2. **Command Classes**: Implement specific command logic
3. **CLI Module**: Handles argument parsing and command execution
4. **Utility Modules**: Provide shared functionality

## Adding a New Command

### Step 1: Create a Command Class

Create a new file in the `commands` directory, e.g., `sigfile_cli/commands/newcommand.py`:

```python
from ..utils.base import BaseCommand
from ..utils.developer_id import get_developer_id

class NewCommand(BaseCommand):
    """Command for managing new functionality"""
    
    def __init__(self):
        super().__init__('newcommand')
        self.required_fields = ['field1', 'field2']
    
    def execute_action(self, field1: str, field2: str) -> str:
        """
        Execute the command action.
        All parameters are required and validated.
        """
        # Create data
        data = {
            'field1': field1,
            'field2': field2,
            'developer_id': get_developer_id()
        }
        
        # Validate required fields
        self.validate_required_fields(data, self.required_fields)
        
        # Save record
        return self.save_record(data)

# Create singleton instance
newcommand = NewCommand()
```

### Step 2: Add the Command to the CLI Module

Update `sigfile_cli/cli.py` to add your new command:

```python
from .commands.newcommand import newcommand

@cli.command()
@click.option('-f1', '--field1', help='First field')
@click.option('-f2', '--field2', help='Second field')
@click.option('-man', '--manual', is_flag=True, help='Show manual page')
@handle_error
def newcommand(field1, field2, manual):
    """Manage new functionality"""
    if manual:
        show_manual('newcommand')
        return

    if not any([field1, field2]):
        # Interactive mode
        try:
            console.print("\n[bold]Executing New Command[/bold]")
            console.print("Press Ctrl+C at any time to cancel\n")
            
            field1 = Prompt.ask("First field")
            field2 = Prompt.ask("Second field")
            
            # Show final command
            console.print("\n[bold]Final Command:[/bold]")
            console.print(f"sigfile newcommand -f1 \"{field1}\" -f2 \"{field2}\"")
            
            if Prompt.ask("\nExecute command?", choices=['y', 'n'], default='y') == 'y':
                filepath = newcommand.execute_action(field1, field2)
                console.print(f"\nAction completed, saved to: {filepath}")
            else:
                console.print("Operation cancelled")
                
        except KeyboardInterrupt:
            console.print("\nOperation cancelled by user")
            sys.exit(0)
    else:
        # Command line mode
        if not all([field1, field2]):
            console.print("[red]Error: All options are required in command line mode[/red]")
            console.print("Try 'sigfile newcommand -man' for usage instructions")
            sys.exit(1)
            
        filepath = newcommand.execute_action(field1, field2)
        console.print(f"\nAction completed, saved to: {filepath}")
```

### Step 3: Create a Manual Page

Create a manual page in `sigfile_cli/man/newcommand.man`:

```
NAME
    sigfile newcommand - Manage new functionality

SYNOPSIS
    sigfile newcommand -f1 FIELD1 -f2 FIELD2
    sigfile newcommand
    sigfile newcommand -man

DESCRIPTION
    The newcommand command manages new functionality.

OPTIONS
    -f1, --field1 FIELD1
        First field (required)

    -f2, --field2 FIELD2
        Second field (required)

    -man, --manual
        Show this manual page

INTERACTIVE MODE
    If no options are provided, the command enters interactive mode and prompts
    for each required field. Press Ctrl+C at any time to cancel.

EXAMPLES
    Execute command:
        sigfile newcommand -f1 "value1" -f2 "value2"

    Interactive mode:
        sigfile newcommand

    View manual:
        sigfile newcommand -man

NOTES
    - All options are required in command line mode
    - Developer ID is automatically determined from git config or system login
    - Records are stored in JSON format with timestamps
    - Each record is immutable once created
```

## Extending the BaseCommand Class

If you need additional functionality for all commands, you can extend the `BaseCommand` class in `utils/base.py`. For example, to add a method for searching records:

```python
def search_records(self, query: str) -> list:
    """
    Search for records matching the query.
    
    Args:
        query: Search query
        
    Returns:
        list: List of matching record filepaths
    """
    try:
        records = self.list_records()
        matches = []
        
        for record_path in records:
            record = self.load_record(record_path)
            if query.lower() in str(record).lower():
                matches.append(record_path)
                
        return matches
        
    except Exception as e:
        raise ValidationError(
            f"Failed to search {self.command_name} records: {str(e)}",
            command=self.command_name
        )
```

## Adding New Utilities

If you need new utility functionality, create a new module in the `utils` directory. For example, to add a utility for formatting output:

```python
# sigfile_cli/utils/formatting.py
from rich.console import Console
from rich.table import Table

console = Console()

def display_table(headers, rows):
    """
    Display data in a formatted table.
    
    Args:
        headers: List of column headers
        rows: List of row data
    """
    table = Table()
    
    for header in headers:
        table.add_column(header)
        
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
        
    console.print(table)
```

## Testing Your Changes

Create tests for your new functionality in the `tests` directory:

```python
# tests/test_newcommand.py
import pytest
from sigfile_cli.commands.newcommand import NewCommand

def test_newcommand_execute_action():
    command = NewCommand()
    filepath = command.execute_action("value1", "value2")
    
    assert filepath.endswith(".json")
    # Add more assertions as needed
```

## Best Practices

1. **Follow the Existing Pattern**: Maintain consistency with the existing code structure.
2. **Validate Inputs**: Always validate required fields and input values.
3. **Handle Errors**: Use the error handling system for consistent error messages.
4. **Document Your Code**: Add docstrings and comments to explain your code.
5. **Create Manual Pages**: Provide clear documentation for users.
6. **Write Tests**: Ensure your code works as expected.
7. **Use Type Hints**: Add type hints to improve code readability and catch errors early. 