import os
import json
from datetime import datetime
from ..utils.base import BaseCommand
from ..utils.developer_id import get_developer_id
from ..utils.error_handling import ValidationError

class DevEnvCommand(BaseCommand):
    """Command for managing development environment"""
    
    def __init__(self):
        super().__init__('devenv')
        self.required_fields = ['role', 'permission', 'action']
    
    def change_permission(self, role: str, permission: str, action: str) -> str:
        """
        Change a permission setting.
        All parameters are required and validated.
        """
        # Create permission change data
        data = {
            'role': role,
            'permission': permission,
            'action': action,
            'developer_id': get_developer_id()
        }
        
        # Validate required fields
        self.validate_required_fields(data, self.required_fields)
        
        # Save permission change
        return self.save_record(data, prefix='permission')

# Create singleton instance
devenv_command = DevEnvCommand() 