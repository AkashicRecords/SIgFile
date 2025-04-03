#!/usr/bin/env python3

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AIAssistant:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.project_dir = os.path.join(self.base_dir, "tracked_projects", project_name)
        self.ai_dir = os.path.join(self.project_dir, "ai_data")
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories for AI data storage."""
        directories = [
            os.path.join(self.ai_dir, "conversations"),
            os.path.join(self.ai_dir, "decisions"),
            os.path.join(self.ai_dir, "datasets"),
            os.path.join(self.ai_dir, "context")
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def log_conversation(self, chat_id: str, messages: List[Dict], code_changes: Optional[List[str]] = None):
        """Log an AI-developer conversation with context."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        conversation_file = os.path.join(self.ai_dir, "conversations", f"chat_{chat_id}_{timestamp}.json")
        
        conversation_data = {
            "chat_id": chat_id,
            "timestamp": timestamp,
            "messages": messages,
            "code_changes": code_changes or [],
            "context": self._get_current_context()
        }
        
        with open(conversation_file, 'w') as f:
            json.dump(conversation_data, f, indent=2)

    def record_decision(self, decision_id: str, description: str, alternatives: List[str], 
                       impact: str, context: str):
        """Record a development decision with alternatives and impact."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        decision_file = os.path.join(self.ai_dir, "decisions", f"decision_{decision_id}_{timestamp}.json")
        
        decision_data = {
            "decision_id": decision_id,
            "timestamp": timestamp,
            "description": description,
            "alternatives": alternatives,
            "impact": impact,
            "context": context
        }
        
        with open(decision_file, 'w') as f:
            json.dump(decision_data, f, indent=2)

    def generate_dataset(self, format: str = "jsonl", include_context: bool = True,
                        filter_tags: Optional[List[str]] = None):
        """Generate a dataset for AI training."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_file = os.path.join(self.ai_dir, "datasets", f"dataset_{timestamp}.{format}")
        
        conversations = self._load_conversations()
        decisions = self._load_decisions()
        
        dataset = self._format_dataset(conversations, decisions, include_context, filter_tags)
        
        with open(dataset_file, 'w') as f:
            if format == "jsonl":
                for item in dataset:
                    f.write(json.dumps(item) + "\n")
            else:
                json.dump(dataset, f, indent=2)

    def _get_current_context(self) -> Dict:
        """Get current development context."""
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "project": self.project_name,
            "recent_changes": self._get_recent_changes(),
            "current_files": self._get_current_files()
        }

    def _get_recent_changes(self) -> List[str]:
        """Get list of recent changes in the project."""
        changes_dir = os.path.join(self.project_dir, "changes")
        if not os.path.exists(changes_dir):
            return []
        
        recent_changes = []
        for date_dir in sorted(os.listdir(changes_dir), reverse=True)[:5]:  # Last 5 days
            date_path = os.path.join(changes_dir, date_dir)
            for change_file in sorted(os.listdir(date_path), reverse=True):
                with open(os.path.join(date_path, change_file), 'r') as f:
                    recent_changes.append(f.read())
        return recent_changes

    def _get_current_files(self) -> List[str]:
        """Get list of currently modified files."""
        # This would need to be implemented based on your version control system
        return []

    def _load_conversations(self) -> List[Dict]:
        """Load all conversation records."""
        conversations = []
        conv_dir = os.path.join(self.ai_dir, "conversations")
        if os.path.exists(conv_dir):
            for file in os.listdir(conv_dir):
                if file.endswith('.json'):
                    with open(os.path.join(conv_dir, file), 'r') as f:
                        conversations.append(json.load(f))
        return conversations

    def _load_decisions(self) -> List[Dict]:
        """Load all decision records."""
        decisions = []
        dec_dir = os.path.join(self.ai_dir, "decisions")
        if os.path.exists(dec_dir):
            for file in os.listdir(dec_dir):
                if file.endswith('.json'):
                    with open(os.path.join(dec_dir, file), 'r') as f:
                        decisions.append(json.load(f))
        return decisions

    def _format_dataset(self, conversations: List[Dict], decisions: List[Dict],
                       include_context: bool, filter_tags: Optional[List[str]]) -> List[Dict]:
        """Format conversations and decisions into a training dataset."""
        dataset = []
        
        # Format conversations
        for conv in conversations:
            if filter_tags and not any(tag in conv.get('tags', []) for tag in filter_tags):
                continue
                
            item = {
                "type": "conversation",
                "chat_id": conv['chat_id'],
                "timestamp": conv['timestamp'],
                "messages": conv['messages'],
                "code_changes": conv['code_changes']
            }
            if include_context:
                item["context"] = conv['context']
            dataset.append(item)
        
        # Format decisions
        for dec in decisions:
            if filter_tags and not any(tag in dec.get('tags', []) for tag in filter_tags):
                continue
                
            item = {
                "type": "decision",
                "decision_id": dec['decision_id'],
                "timestamp": dec['timestamp'],
                "description": dec['description'],
                "alternatives": dec['alternatives'],
                "impact": dec['impact']
            }
            if include_context:
                item["context"] = dec['context']
            dataset.append(item)
        
        return dataset

def main():
    """Command-line interface for AI Assistant features."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Development Assistant')
    parser.add_argument('-p', '--project', required=True, help='Project name')
    parser.add_argument('command', choices=['log', 'decide', 'dataset'], help='Command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')
    
    args = parser.parse_args()
    assistant = AIAssistant(args.project)
    
    if args.command == 'log':
        if len(args.args) < 2:
            print("Usage: ai_assistant.py -p project log <chat_id> <messages_json> [code_changes]")
            return
        chat_id = args.args[0]
        messages = json.loads(args.args[1])
        code_changes = json.loads(args.args[2]) if len(args.args) > 2 else None
        assistant.log_conversation(chat_id, messages, code_changes)
    
    elif args.command == 'decide':
        if len(args.args) < 4:
            print("Usage: ai_assistant.py -p project decide <decision_id> <description> <alternatives_json> <impact> <context>")
            return
        decision_id = args.args[0]
        description = args.args[1]
        alternatives = json.loads(args.args[2])
        impact = args.args[3]
        context = args.args[4]
        assistant.record_decision(decision_id, description, alternatives, impact, context)
    
    elif args.command == 'dataset':
        format = args.args[0] if args.args else "jsonl"
        include_context = args.args[1].lower() == "true" if len(args.args) > 1 else True
        filter_tags = json.loads(args.args[2]) if len(args.args) > 2 else None
        assistant.generate_dataset(format, include_context, filter_tags)

if __name__ == '__main__':
    main() 