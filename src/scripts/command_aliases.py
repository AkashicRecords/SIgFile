#!/usr/bin/env python3

import os
import sys
from typing import Dict, List, Optional
import json
from pathlib import Path

# Default aliases configuration
DEFAULT_ALIASES = {
    # Change tracking aliases
    'track': 'python src/scripts/track_change.py record',
    'backup': 'python src/scripts/track_change.py backup',
    'history': 'python src/scripts/track_change.py history',
    
    # Decision tracking aliases
    'decision': 'python src/scripts/cli.py decision',
    'decide': 'python src/scripts/cli.py decision -n',
    
    # AI session aliases
    'ai-start': 'python src/scripts/track_change.py ai-record',
    'ai-stop': 'python src/scripts/track_change.py ai-stop',
    'ai-history': 'python src/scripts/track_change.py ai-history',
    
    # Project management aliases
    'project-start': 'python src/scripts/track_change.py setup',
    'project-status': 'python src/scripts/track_change.py status',
    
    # Quick commands
    'quick-track': 'python src/scripts/track_change.py record "quick"',
    'quick-backup': 'python src/scripts/track_change.py backup --quick',
    
    # IDE-specific aliases
    'ide-track': 'python src/scripts/track_change.py record "ide"',
    'ide-backup': 'python src/scripts/track_change.py backup --ide',
}

class CommandAliases:
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize command aliases system."""
        self.config_dir = config_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'config'
        )
        self.aliases_file = os.path.join(self.config_dir, 'aliases.json')
        self.aliases = self._load_aliases()
    
    def _load_aliases(self) -> Dict[str, str]:
        """Load aliases from config file or create default."""
        if os.path.exists(self.aliases_file):
            with open(self.aliases_file, 'r') as f:
                return json.load(f)
        return DEFAULT_ALIASES.copy()
    
    def _save_aliases(self) -> None:
        """Save current aliases to config file."""
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.aliases_file, 'w') as f:
            json.dump(self.aliases, f, indent=2)
    
    def add_alias(self, name: str, command: str) -> None:
        """Add a new alias."""
        self.aliases[name] = command
        self._save_aliases()
    
    def remove_alias(self, name: str) -> None:
        """Remove an alias."""
        if name in self.aliases:
            del self.aliases[name]
            self._save_aliases()
    
    def get_alias(self, name: str) -> Optional[str]:
        """Get command for an alias."""
        return self.aliases.get(name)
    
    def list_aliases(self) -> Dict[str, str]:
        """List all current aliases."""
        return self.aliases.copy()
    
    def execute_alias(self, name: str, args: List[str]) -> None:
        """Execute an alias with additional arguments."""
        if name not in self.aliases:
            print(f"Error: Alias '{name}' not found")
            return
        
        command = self.aliases[name]
        if args:
            command = f"{command} {' '.join(args)}"
        
        os.system(command)

def main():
    """Main entry point for command aliases."""
    if len(sys.argv) < 2:
        print("Usage: python command_aliases.py <alias_name> [args...]")
        return
    
    aliases = CommandAliases()
    alias_name = sys.argv[1]
    args = sys.argv[2:]
    
    aliases.execute_alias(alias_name, args)

if __name__ == '__main__':
    main() 