#!/usr/bin/env python3

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

class DecisionTracker:
    """Handles tracking and analysis of project decisions."""
    
    def __init__(self, project_name: str):
        """
        Initialize decision tracking for a project.
        
        Args:
            project_name: Name of the project to track
        """
        self.project_name = project_name
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.decisions_dir = os.path.join(self.base_dir, "tracked_projects", project_name, "decisions")
        os.makedirs(self.decisions_dir, exist_ok=True)
    
    def record_decision(self, decision_id: str, description: str, rationale: str,
                       alternatives: List[Dict[str, str]], impact: Dict[str, Any],
                       code_changes: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Record a project decision with associated information.
        
        Args:
            decision_id: Unique identifier for the decision
            description: Description of the decision
            rationale: Rationale behind the decision
            alternatives: List of alternative approaches considered
            impact: Dictionary containing impact assessment
            code_changes: Optional list of associated code changes
        
        Returns:
            Path to the saved decision file
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        decision_data = {
            'decision_id': decision_id,
            'project_name': self.project_name,
            'timestamp': timestamp,
            'date': date,
            'description': description,
            'rationale': rationale,
            'alternatives': alternatives,
            'impact': impact,
            'code_changes': code_changes or [],
            'related_decisions': self._find_related_decisions(description, rationale),
            'implementation_plan': self._generate_implementation_plan(description, impact),
            'success_criteria': self._generate_success_criteria(description, impact)
        }
        
        # Save decision
        decision_file = os.path.join(
            self.decisions_dir,
            f"decision_{decision_id}_{timestamp}.json"
        )
        with open(decision_file, 'w') as f:
            json.dump(decision_data, f, indent=2)
        
        return decision_file
    
    def analyze_decisions(self) -> Dict[str, Any]:
        """
        Analyze all recorded decisions to extract insights.
        
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'total_decisions': 0,
            'decisions_by_month': defaultdict(int),
            'impact_areas': defaultdict(int),
            'common_alternatives': defaultdict(int),
            'implementation_status': defaultdict(int),
            'code_changes': {
                'total': 0,
                'by_type': defaultdict(int),
                'by_file': defaultdict(int)
            },
            'related_decisions': defaultdict(list)
        }
        
        # Analyze each decision
        for decision_file in Path(self.decisions_dir).glob("decision_*.json"):
            with open(decision_file, 'r') as f:
                decision_data = json.load(f)
            
            analysis['total_decisions'] += 1
            
            # Track decisions by month
            date = datetime.datetime.strptime(decision_data['date'], "%Y-%m-%d")
            month_key = date.strftime("%Y-%m")
            analysis['decisions_by_month'][month_key] += 1
            
            # Track impact areas
            for area in decision_data['impact'].get('areas', []):
                analysis['impact_areas'][area] += 1
            
            # Track alternatives considered
            for alt in decision_data.get('alternatives', []):
                analysis['common_alternatives'][alt.get('type', 'unknown')] += 1
            
            # Track code changes
            for change in decision_data.get('code_changes', []):
                analysis['code_changes']['total'] += 1
                analysis['code_changes']['by_type'][change.get('type', 'unknown')] += 1
                analysis['code_changes']['by_file'][change.get('file', 'unknown')] += 1
            
            # Track related decisions
            decision_id = decision_data['decision_id']
            related = decision_data.get('related_decisions', [])
            if related:
                analysis['related_decisions'][decision_id] = related
        
        # Convert defaultdicts to regular dicts for JSON serialization
        analysis['decisions_by_month'] = dict(analysis['decisions_by_month'])
        analysis['impact_areas'] = dict(analysis['impact_areas'])
        analysis['common_alternatives'] = dict(analysis['common_alternatives'])
        analysis['implementation_status'] = dict(analysis['implementation_status'])
        analysis['code_changes']['by_type'] = dict(analysis['code_changes']['by_type'])
        analysis['code_changes']['by_file'] = dict(analysis['code_changes']['by_file'])
        analysis['related_decisions'] = dict(analysis['related_decisions'])
        
        return analysis
    
    def _find_related_decisions(self, description: str, rationale: str) -> List[str]:
        """Find related decisions based on description and rationale."""
        # This is a placeholder for more sophisticated related decision finding
        return []
    
    def _generate_implementation_plan(self, description: str, impact: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an implementation plan based on decision details."""
        # This is a placeholder for more sophisticated implementation plan generation
        return {
            'steps': [],
            'timeline': 'TBD',
            'resources': [],
            'risks': []
        }
    
    def _generate_success_criteria(self, description: str, impact: Dict[str, Any]) -> List[str]:
        """Generate success criteria based on decision details."""
        # This is a placeholder for more sophisticated success criteria generation
        return []

def main():
    """Command line interface for decision tracking."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Project decision tracking and analysis')
    parser.add_argument('project_name',
                       help='Name of the project to track')
    parser.add_argument('command', choices=['record', 'analyze'],
                       help='Command to execute')
    parser.add_argument('--decision-id',
                       help='Decision ID for recording')
    parser.add_argument('--description',
                       help='Decision description')
    parser.add_argument('--rationale',
                       help='Decision rationale')
    parser.add_argument('--alternatives-file',
                       help='JSON file containing alternative approaches')
    parser.add_argument('--impact-file',
                       help='JSON file containing impact assessment')
    parser.add_argument('--changes-file',
                       help='JSON file containing code changes')
    
    args = parser.parse_args()
    
    tracker = DecisionTracker(args.project_name)
    
    if args.command == 'record':
        if not (args.decision_id and args.description and args.rationale and
                args.alternatives_file and args.impact_file):
            parser.error("record command requires --decision-id, --description, --rationale, "
                       "--alternatives-file, and --impact-file")
        
        # Load alternatives
        with open(args.alternatives_file, 'r') as f:
            alternatives = json.load(f)
        
        # Load impact assessment
        with open(args.impact_file, 'r') as f:
            impact = json.load(f)
        
        # Load code changes if provided
        code_changes = None
        if args.changes_file:
            with open(args.changes_file, 'r') as f:
                code_changes = json.load(f)
        
        # Record decision
        output_file = tracker.record_decision(
            args.decision_id,
            args.description,
            args.rationale,
            alternatives,
            impact,
            code_changes
        )
        print(f"Decision recorded to: {output_file}")
    
    elif args.command == 'analyze':
        analysis = tracker.analyze_decisions()
        print(json.dumps(analysis, indent=2))

if __name__ == '__main__':
    main() 