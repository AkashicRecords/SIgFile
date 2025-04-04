import os
import json
from datetime import datetime
from ..utils.base import BaseCommand
from ..utils.developer_id import get_developer_id
from ..utils.error_handling import ValidationError

class DecisionCommand(BaseCommand):
    """Command for managing development decisions"""
    
    def __init__(self):
        super().__init__('decision')
        self.required_fields = ['title', 'type', 'priority']
    
    def create_decision(self, title: str, type: str, priority: str) -> str:
        """
        Create a new decision with the given parameters.
        All parameters are required and validated.
        """
        # Create decision data
        data = {
            'title': title,
            'type': type,
            'priority': priority,
            'developer_id': get_developer_id(),
            'status': 'pending'
        }
        
        # Validate required fields
        self.validate_required_fields(data, self.required_fields)
        
        # Save decision
        return self.save_record(data)

# Create singleton instance
decision_command = DecisionCommand()

def decision_command(title, type, priority):
    """
    Create a new decision with the given parameters.
    All parameters are required and validated.
    """
    # Validate inputs
    if not all([title, type, priority]):
        raise ValidationError(
            "All parameters (title, type, priority) are required",
            command="decision"
        )
    
    # Get developer ID
    developer_id = get_developer_id()
    
    # Create decision record
    decision = {
        "title": title,
        "type": type,
        "priority": priority,
        "developer_id": developer_id,
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }
    
    # Save decision
    try:
        # Ensure directory exists
        os.makedirs("decisions", exist_ok=True)
        
        # Create filename from timestamp
        filename = f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join("decisions", filename)
        
        # Write decision to file
        with open(filepath, 'w') as f:
            json.dump(decision, f, indent=2)
            
        return filepath
        
    except Exception as e:
        raise ValidationError(
            f"Failed to save decision: {str(e)}",
            command="decision"
        ) 