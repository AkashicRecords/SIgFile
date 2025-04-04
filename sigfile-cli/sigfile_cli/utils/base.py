import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from .error_handling import ValidationError

class BaseCommand:
    """Base class for all CLI commands with common functionality"""
    
    def __init__(self, command_name: str):
        self.command_name = command_name
        self.storage_dir = command_name + 's'  # e.g., 'decisions', 'permissions'
        
    def save_record(self, data: Dict[str, Any], prefix: Optional[str] = None) -> str:
        """
        Save a record to JSON file with standard naming and structure.
        
        Args:
            data: The data to save
            prefix: Optional prefix for the filename (defaults to command name)
            
        Returns:
            str: Path to the saved file
        """
        try:
            # Ensure directory exists
            os.makedirs(self.storage_dir, exist_ok=True)
            
            # Create filename from timestamp with optional prefix
            prefix = prefix or self.command_name
            filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.storage_dir, filename)
            
            # Add standard metadata
            full_record = {
                **data,
                "timestamp": datetime.now().isoformat(),
                "command": self.command_name
            }
            
            # Write to file
            with open(filepath, 'w') as f:
                json.dump(full_record, f, indent=2)
                
            return filepath
            
        except Exception as e:
            raise ValidationError(
                f"Failed to save {self.command_name} record: {str(e)}",
                command=self.command_name
            )
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: list) -> None:
        """
        Validate that all required fields are present and non-empty.
        
        Args:
            data: Dictionary of field values
            required_fields: List of required field names
        """
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing)}",
                command=self.command_name
            )
    
    def load_record(self, filepath: str) -> Dict[str, Any]:
        """
        Load a record from JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            dict: The loaded record
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise ValidationError(
                f"Failed to load {self.command_name} record: {str(e)}",
                command=self.command_name
            )
    
    def list_records(self) -> list:
        """
        List all records for this command.
        
        Returns:
            list: List of record filepaths
        """
        try:
            if not os.path.exists(self.storage_dir):
                return []
            return sorted([
                os.path.join(self.storage_dir, f)
                for f in os.listdir(self.storage_dir)
                if f.endswith('.json')
            ])
        except Exception as e:
            raise ValidationError(
                f"Failed to list {self.command_name} records: {str(e)}",
                command=self.command_name
            ) 