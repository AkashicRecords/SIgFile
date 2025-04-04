from typing import Dict, List, Optional
import json
from pathlib import Path
from datetime import datetime
import logging
from .record_manager import RecordManager, RecordEntry

class AIRecordAssistant:
    """Assists in gathering manual input for records through AI interaction."""
    
    def __init__(self, record_manager: RecordManager):
        self.manager = record_manager
        self.logger = logging.getLogger(__name__)
        self.pending_inputs = {}
    
    def _create_ai_prompt(self, record_type: str, required_fields: Dict[str, str]) -> str:
        """Create a prompt for the AI to gather required information."""
        prompt = f"""Please help gather information for a {record_type} record.
Required fields and their purposes:
"""
        for field, purpose in required_fields.items():
            prompt += f"- {field}: {purpose}\n"
        
        prompt += """
Please ask the developer for each piece of information in a conversational way.
After gathering all information, format it as a JSON object with the following structure:
{
    "field_name": "developer's response",
    ...
}
"""
        return prompt
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse the AI's response containing gathered information."""
        try:
            # Extract JSON from response
            json_str = response[response.find('{'):response.rfind('}')+1]
            return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Error parsing AI response: {str(e)}")
            return {}
    
    async def gather_decision_input(self) -> Dict:
        """Gather required input for a decision record through AI interaction."""
        required_fields = {
            "title": "Short, descriptive title of the decision",
            "context": "Background and context for the decision",
            "decision": "The actual decision made",
            "rationale": "Reasoning behind the decision",
            "alternatives": "Other options considered",
            "consequences": "Expected impact of the decision"
        }
        
        prompt = self._create_ai_prompt("decision", required_fields)
        # Here we would send the prompt to the AI and get a response
        # For now, we'll simulate the interaction
        ai_response = await self._simulate_ai_interaction(prompt)
        return self._parse_ai_response(ai_response)
    
    async def gather_change_input(self, affected_files: List[str]) -> Dict:
        """Gather required input for a change record through AI interaction."""
        required_fields = {
            "description": "Description of the changes made",
            "purpose": "Purpose and goal of the changes",
            "impact": "Expected impact on the system",
            "testing": "Testing performed or needed",
            "verification": "How to verify the changes"
        }
        
        prompt = self._create_ai_prompt("change", required_fields)
        prompt += f"\nAffected files:\n" + "\n".join(f"- {file}" for file in affected_files)
        
        ai_response = await self._simulate_ai_interaction(prompt)
        return self._parse_ai_response(ai_response)
    
    async def gather_debug_input(self, issue_description: str) -> Dict:
        """Gather required input for a debug record through AI interaction."""
        required_fields = {
            "root_cause": "Root cause of the issue",
            "solution": "Solution implemented",
            "prevention": "Measures to prevent recurrence",
            "testing": "Testing performed to verify fix",
            "documentation": "Documentation updates needed"
        }
        
        prompt = self._create_ai_prompt("debug", required_fields)
        prompt += f"\nIssue description: {issue_description}"
        
        ai_response = await self._simulate_ai_interaction(prompt)
        return self._parse_ai_response(ai_response)
    
    async def create_decision_record_with_ai(self, author: str) -> str:
        """Create a decision record with AI-assisted input gathering."""
        try:
            # Gather required information through AI
            inputs = await self.gather_decision_input()
            
            # Create the record
            return self.manager.create_decision_record(
                title=inputs.get('title', ''),
                context=inputs.get('context', ''),
                decision=inputs.get('decision', ''),
                author=author,
                related_files=inputs.get('related_files', [])
            )
        except Exception as e:
            self.logger.error(f"Error creating decision record: {str(e)}")
            raise
    
    async def create_change_record_with_ai(self, 
                                         files: List[str],
                                         author: str) -> str:
        """Create a change record with AI-assisted input gathering."""
        try:
            # Gather required information through AI
            inputs = await self.gather_change_input(files)
            
            # Create the record
            return self.manager.create_change_record(
                description=inputs.get('description', ''),
                author=author,
                files=files,
                changes=inputs.get('changes', {})
            )
        except Exception as e:
            self.logger.error(f"Error creating change record: {str(e)}")
            raise
    
    async def create_debug_record_with_ai(self,
                                        issue: str,
                                        author: str) -> str:
        """Create a debug record with AI-assisted input gathering."""
        try:
            # Gather required information through AI
            inputs = await self.gather_debug_input(issue)
            
            # Create the record
            return self.manager.create_debug_record(
                issue=issue,
                author=author,
                solution=inputs.get('solution', ''),
                related_files=inputs.get('related_files', [])
            )
        except Exception as e:
            self.logger.error(f"Error creating debug record: {str(e)}")
            raise
    
    async def _simulate_ai_interaction(self, prompt: str) -> str:
        """Simulate AI interaction for testing purposes."""
        # In a real implementation, this would send the prompt to an AI service
        # and return the response. For now, we'll return a simulated response.
        return """
        {
            "title": "Implement AI-Assisted Record Creation",
            "context": "Need to automate gathering of manual input for records",
            "decision": "Create AI assistant to gather required information",
            "rationale": "Reduces manual effort and ensures completeness",
            "alternatives": ["Manual forms", "Template-based input"],
            "consequences": "Improved record quality and consistency"
        }
        """ 