import functools
import sys
from rich.console import Console

console = Console()

class SigFileError(Exception):
    """Base exception for SigFile CLI errors"""
    def __init__(self, message, command=None):
        self.message = message
        self.command = command
        super().__init__(self.message)

class ValidationError(SigFileError):
    """Raised when command validation fails"""
    pass

class ConfigurationError(SigFileError):
    """Raised when there's a configuration issue"""
    pass

def handle_error(func):
    """Decorator for consistent error handling across commands"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SigFileError as e:
            console.print(f"\n[red]Error: {e.message}[/red]")
            if e.command:
                console.print(f"\nTry 'sigfile {e.command} -man' for usage instructions")
            sys.exit(1)
        except KeyboardInterrupt:
            console.print("\nOperation cancelled by user")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[red]Unexpected error: {str(e)}[/red]")
            console.print("\nPlease report this issue with the following information:")
            console.print(f"Command: {func.__name__}")
            console.print(f"Error: {str(e)}")
            sys.exit(1)
    return wrapper 