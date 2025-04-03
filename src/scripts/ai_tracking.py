#!/usr/bin/env python3

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

class AITracking:
    """Handles tracking and analysis of AI conversations."""
    
    def __init__(self, project_name: str):
        """
        Initialize AI tracking for a project.
        
        Args:
            project_name: Name of the project to track
        """
        self.project_name = project_name
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.conversations_dir = os.path.join(self.base_dir, "tracked_projects", project_name, "ai_conversations")
        os.makedirs(self.conversations_dir, exist_ok=True)
    
    def record_conversation(self, chat_id: str, messages: List[Dict[str, str]], code_changes: List[Dict[str, str]]) -> str:
        """
        Record an AI conversation with associated code changes.
        
        Args:
            chat_id: Unique identifier for the conversation
            messages: List of message dictionaries with 'role' and 'content'
            code_changes: List of code change dictionaries with 'file', 'type', and 'content'
        
        Returns:
            Path to the saved conversation file
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        conversation_data = {
            'chat_id': chat_id,
            'project_name': self.project_name,
            'timestamp': timestamp,
            'date': date,
            'messages': messages,
            'code_changes': code_changes,
            'summary': self._generate_summary(messages),
            'key_decisions': self._extract_decisions(messages),
            'common_topics': self._analyze_topics(messages),
            'impact_areas': self._analyze_impact(messages, code_changes),
            'next_steps': self._extract_next_steps(messages)
        }
        
        # Save conversation
        conversation_file = os.path.join(
            self.conversations_dir,
            f"conversation_{chat_id}_{timestamp}.json"
        )
        with open(conversation_file, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        return conversation_file
    
    def generate_dataset(self, format: str = "jsonl", include_code: bool = False) -> str:
        """
        Generate a dataset from recorded conversations.
        
        Args:
            format: Output format ('jsonl' or 'json')
            include_code: Whether to include code changes in the dataset
        
        Returns:
            Path to the generated dataset file
        """
        dataset = []
        
        # Collect all conversations
        for conv_file in Path(self.conversations_dir).glob("conversation_*.json"):
            with open(conv_file, 'r') as f:
                conv_data = json.load(f)
            
            # Filter out code changes if not included
            if not include_code:
                conv_data.pop('code_changes', None)
            
            dataset.append(conv_data)
        
        # Save dataset
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_file = os.path.join(
            self.conversations_dir,
            f"dataset_{timestamp}.{format}"
        )
        
        if format == "jsonl":
            with open(dataset_file, 'w') as f:
                for item in dataset:
                    f.write(json.dumps(item) + '\n')
        else:
            with open(dataset_file, 'w') as f:
                json.dump(dataset, f, indent=2)
        
        return dataset_file
    
    def analyze_conversations(self) -> Dict[str, Any]:
        """
        Analyze all recorded conversations to extract insights.
        
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'total_conversations': 0,
            'total_messages': 0,
            'common_topics': defaultdict(int),
            'impact_areas': defaultdict(int),
            'code_changes': {
                'total': 0,
                'by_type': defaultdict(int),
                'by_file': defaultdict(int)
            },
            'decisions': {
                'total': 0,
                'by_type': defaultdict(int)
            }
        }
        
        # Analyze each conversation
        for conv_file in Path(self.conversations_dir).glob("conversation_*.json"):
            with open(conv_file, 'r') as f:
                conv_data = json.load(f)
            
            analysis['total_conversations'] += 1
            analysis['total_messages'] += len(conv_data.get('messages', []))
            
            # Analyze topics
            for topic in conv_data.get('common_topics', []):
                analysis['common_topics'][topic] += 1
            
            # Analyze impact areas
            for area in conv_data.get('impact_areas', []):
                analysis['impact_areas'][area] += 1
            
            # Analyze code changes
            for change in conv_data.get('code_changes', []):
                analysis['code_changes']['total'] += 1
                analysis['code_changes']['by_type'][change.get('type', 'unknown')] += 1
                analysis['code_changes']['by_file'][change.get('file', 'unknown')] += 1
            
            # Analyze decisions
            decisions = conv_data.get('key_decisions', [])
            analysis['decisions']['total'] += len(decisions)
            for decision in decisions:
                analysis['decisions']['by_type'][decision.get('type', 'unknown')] += 1
        
        # Convert defaultdicts to regular dicts for JSON serialization
        analysis['common_topics'] = dict(analysis['common_topics'])
        analysis['impact_areas'] = dict(analysis['impact_areas'])
        analysis['code_changes']['by_type'] = dict(analysis['code_changes']['by_type'])
        analysis['code_changes']['by_file'] = dict(analysis['code_changes']['by_file'])
        analysis['decisions']['by_type'] = dict(analysis['decisions']['by_type'])
        
        return analysis
    
    def _generate_summary(self, messages: List[Dict[str, str]]) -> str:
        """Generate a summary of the conversation."""
        # This is a placeholder for more sophisticated summarization
        return "Conversation summary placeholder"
    
    def _extract_decisions(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Extract key decisions from the conversation."""
        # This is a placeholder for more sophisticated decision extraction
        return []
    
    def _analyze_topics(self, messages: List[Dict[str, str]]) -> List[str]:
        """Analyze common topics in the conversation."""
        # This is a placeholder for more sophisticated topic analysis
        return []
    
    def _analyze_impact(self, messages: List[Dict[str, str]], code_changes: List[Dict[str, str]]) -> List[str]:
        """Analyze impact areas of the conversation and code changes."""
        # This is a placeholder for more sophisticated impact analysis
        return []
    
    def _extract_next_steps(self, messages: List[Dict[str, str]]) -> List[str]:
        """Extract next steps from the conversation."""
        # This is a placeholder for more sophisticated next steps extraction
        return []

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