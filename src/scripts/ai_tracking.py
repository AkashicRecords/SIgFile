#!/usr/bin/env python3

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AITracking:
    """Handles tracking and analysis of AI conversations."""
    
    def __init__(self, project_name: str):
        """
        Initialize AI tracking for a project.
        
        Args:
            project_name: Name of the project to track
        """
        self.project_name = project_name
        self.base_dir = Path('tracked_projects') / project_name
        self.ai_dir = self.base_dir / 'ai_conversations'
        self.thinking_dir = self.base_dir / 'thinking'
        
        # Create directories if they don't exist
        self.ai_dir.mkdir(parents=True, exist_ok=True)
        self.thinking_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize session tracking
        self.current_session = None
        self.session_start = None
        self.session_data = []
    
    def start_session(self, session_name: str, description: str) -> None:
        """Start a new AI session."""
        self.current_session = session_name
        self.session_start = datetime.now()
        self.session_data = []
        
        # Create session file
        session_file = self.ai_dir / f"{session_name}_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        initial_data = {
            "session_name": session_name,
            "description": description,
            "start_time": self.session_start.isoformat(),
            "events": []
        }
        
        with open(session_file, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def end_session(self) -> None:
        """End the current AI session."""
        if not self.current_session:
            return
        
        end_time = datetime.now()
        session_file = self.ai_dir / f"{self.current_session}_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        
        if session_file.exists():
            with open(session_file, 'r') as f:
                data = json.load(f)
            
            data["end_time"] = end_time.isoformat()
            data["duration_seconds"] = (end_time - self.session_start).total_seconds()
            
            with open(session_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        self.current_session = None
        self.session_start = None
        self.session_data = []

    def record_event(self, event_type: str, content: Dict) -> None:
        """Record an event in the current session."""
        if not self.current_session:
            return
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "content": content
        }
        
        self.session_data.append(event)
        
        # Update session file
        session_file = self.ai_dir / f"{self.current_session}_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        if session_file.exists():
            with open(session_file, 'r') as f:
                data = json.load(f)
            
            data["events"].append(event)
            
            with open(session_file, 'w') as f:
                json.dump(data, f, indent=2)

    def record_thinking(self, thought: str, context: Optional[Dict] = None) -> None:
        """Record a thinking process."""
        timestamp = datetime.now()
        thought_file = self.thinking_dir / f"thought_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        
        thought_data = {
            "timestamp": timestamp.isoformat(),
            "thought": thought,
            "context": context or {}
        }
        
        with open(thought_file, 'w') as f:
            json.dump(thought_data, f, indent=2)

    def get_session_history(self, session_name: Optional[str] = None) -> List[Dict]:
        """Get history of AI sessions."""
        sessions = []
        for file in self.ai_dir.glob("*.json"):
            with open(file, 'r') as f:
                data = json.load(f)
                if session_name is None or data["session_name"] == session_name:
                    sessions.append(data)
        return sorted(sessions, key=lambda x: x["start_time"])

    def get_thinking_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get history of thinking processes."""
        thoughts = []
        for file in sorted(self.thinking_dir.glob("*.json"), reverse=True):
            with open(file, 'r') as f:
                thoughts.append(json.load(f))
            if limit and len(thoughts) >= limit:
                break
        return thoughts

def main():
    """Command line interface for AI tracking."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI conversation tracking and analysis')
    parser.add_argument('project_name',
                       help='Name of the project to track')
    parser.add_argument('command', choices=['record', 'dataset', 'analyze'],
                       help='Command to execute')
    parser.add_argument('--chat-id',
                       help='Chat ID for recording conversation')
    parser.add_argument('--messages-file',
                       help='JSON file containing conversation messages')
    parser.add_argument('--changes-file',
                       help='JSON file containing code changes')
    parser.add_argument('--format', choices=['json', 'jsonl'], default='jsonl',
                       help='Output format for dataset generation')
    parser.add_argument('--include-code', action='store_true',
                       help='Include code changes in dataset')
    
    args = parser.parse_args()
    
    tracker = AITracking(args.project_name)
    
    if args.command == 'record':
        if not (args.chat_id and args.messages_file):
            parser.error("record command requires --chat-id and --messages-file")
        
        # Load messages
        with open(args.messages_file, 'r') as f:
            messages = json.load(f)
        
        # Load code changes if provided
        code_changes = []
        if args.changes_file:
            with open(args.changes_file, 'r') as f:
                code_changes = json.load(f)
        
        # Record conversation
        output_file = tracker.record_conversation(args.chat_id, messages, code_changes)
        print(f"Conversation recorded to: {output_file}")
    
    elif args.command == 'dataset':
        output_file = tracker.generate_dataset(args.format, args.include_code)
        print(f"Dataset generated at: {output_file}")
    
    elif args.command == 'analyze':
        analysis = tracker.analyze_conversations()
        print(json.dumps(analysis, indent=2))

if __name__ == '__main__':
    main() 