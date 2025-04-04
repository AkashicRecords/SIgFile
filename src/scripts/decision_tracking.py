#!/usr/bin/env python3

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class DecisionTracker:
    def __init__(self, project_name: str = "logiclens"):
        """Initialize decision tracker for a project."""
        self.project_name = project_name
        self.project_root = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.decisions_dir = self.project_root / "tracked_projects" / project_name / "decisions"
        self.decisions_dir.mkdir(parents=True, exist_ok=True)

    def record_decision(self, title: str, description: str, context: Optional[Dict] = None) -> str:
        """Record a new decision."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        decision_id = f"decision_{timestamp}"
        
        decision = {
            "id": decision_id,
            "title": title,
            "description": description,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "project": self.project_name
        }
        
        decision_file = self.decisions_dir / f"{decision_id}.json"
        with open(decision_file, 'w') as f:
            json.dump(decision, f, indent=2)
        
        return decision_id

    def get_decision(self, decision_id: str) -> Optional[Dict]:
        """Get a specific decision by ID."""
        decision_file = self.decisions_dir / f"{decision_id}.json"
        if decision_file.exists():
            with open(decision_file) as f:
                return json.load(f)
        return None

    def list_decisions(self, limit: Optional[int] = None) -> List[Dict]:
        """List all decisions, optionally limited to a specific number."""
        decisions = []
        for decision_file in sorted(self.decisions_dir.glob("decision_*.json"), reverse=True):
            with open(decision_file) as f:
                decisions.append(json.load(f))
            if limit and len(decisions) >= limit:
                break
        return decisions

    def search_decisions(self, query: str) -> List[Dict]:
        """Search decisions by title or description."""
        query = query.lower()
        matching_decisions = []
        
        for decision in self.list_decisions():
            if (query in decision['title'].lower() or 
                query in decision['description'].lower()):
                matching_decisions.append(decision)
        
        return matching_decisions

def main():
    """CLI interface for decision tracking."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Track project decisions')
    parser.add_argument('--project', default='logiclens', help='Project name')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Record command
    record_parser = subparsers.add_parser('record', help='Record a new decision')
    record_parser.add_argument('title', help='Decision title')
    record_parser.add_argument('description', help='Decision description')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List decisions')
    list_parser.add_argument('--limit', type=int, help='Limit number of decisions')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search decisions')
    search_parser.add_argument('query', help='Search query')
    
    args = parser.parse_args()
    tracker = DecisionTracker(args.project)
    
    if args.command == 'record':
        decision_id = tracker.record_decision(args.title, args.description)
        print(f"Decision recorded with ID: {decision_id}")
    
    elif args.command == 'list':
        decisions = tracker.list_decisions(args.limit)
        for decision in decisions:
            print(f"\nDecision: {decision['id']}")
            print(f"Title: {decision['title']}")
            print(f"Description: {decision['description']}")
            print(f"Timestamp: {decision['timestamp']}")
    
    elif args.command == 'search':
        decisions = tracker.search_decisions(args.query)
        print(f"Found {len(decisions)} matching decisions:")
        for decision in decisions:
            print(f"\nDecision: {decision['id']}")
            print(f"Title: {decision['title']}")
            print(f"Description: {decision['description']}")

if __name__ == '__main__':
    main() 