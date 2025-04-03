#!/usr/bin/env python3

import os
import json
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader

class TemplateRenderer:
    """Handles rendering of AI conversation and decision templates."""
    
    def __init__(self):
        """Initialize template environment."""
        template_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'templates'
        )
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def render_ai_conversation(self, data: Dict[str, Any], output_file: str) -> None:
        """
        Render an AI conversation template with the provided data.
        
        Args:
            data: Dictionary containing conversation data
            output_file: Path to save the rendered template
        """
        required_fields = [
            'chat_id',
            'project_name',
            'summary',
            'key_decisions',
            'code_changes',
            'related_changes',
            'next_steps',
            'ai_insights'
        ]
        
        # Ensure all required fields are present
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Add timestamp if not provided
        if 'timestamp' not in data:
            data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'date' not in data:
            data['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Render template
        template = self.env.get_template('ai_conversation_template.md')
        rendered = template.render(**data)
        
        # Save to file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(rendered)
    
    def render_decision(self, data: Dict[str, Any], output_file: str) -> None:
        """
        Render a decision template with the provided data.
        
        Args:
            data: Dictionary containing decision data
            output_file: Path to save the rendered template
        """
        required_fields = [
            'decision_id',
            'project_name',
            'description',
            'rationale',
            'impact',
            'alternatives',
            'code_changes',
            'related_decisions',
            'implementation_plan',
            'success_criteria'
        ]
        
        # Ensure all required fields are present
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Add timestamp if not provided
        if 'timestamp' not in data:
            data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'date' not in data:
            data['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Render template
        template = self.env.get_template('decision_template.md')
        rendered = template.render(**data)
        
        # Save to file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(rendered)

def main():
    """Command line interface for template rendering."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Template renderer for AI conversations and decisions')
    parser.add_argument('template_type', choices=['ai', 'decision'],
                       help='Type of template to render')
    parser.add_argument('data_file',
                       help='JSON file containing template data')
    parser.add_argument('output_file',
                       help='Path to save rendered template')
    
    args = parser.parse_args()
    
    # Load data
    with open(args.data_file, 'r') as f:
        data = json.load(f)
    
    # Initialize renderer
    renderer = TemplateRenderer()
    
    # Render template
    if args.template_type == 'ai':
        renderer.render_ai_conversation(data, args.output_file)
    else:
        renderer.render_decision(data, args.output_file)

if __name__ == '__main__':
    main() 