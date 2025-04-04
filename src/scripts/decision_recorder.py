#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import stat
from datetime import datetime
from typing import List, Dict, Optional

class DecisionRecorder:
    """Records decisions with automated code analysis."""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.decisions_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'tracked_projects',
            project_name,
            'decisions'
        )
        self._verify_and_create_directory()
        
    def _verify_and_create_directory(self):
        """Verify and create decisions directory with proper permissions."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.decisions_dir, exist_ok=True)
            
            # Set directory permissions (755)
            os.chmod(self.decisions_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            
            # Verify directory exists and is writable
            if not os.path.exists(self.decisions_dir):
                raise PermissionError(f"Failed to create directory: {self.decisions_dir}")
            if not os.access(self.decisions_dir, os.W_OK):
                raise PermissionError(f"Directory not writable: {self.decisions_dir}")
                
            print(f"Decisions directory verified: {self.decisions_dir}")
        except Exception as e:
            print(f"Error verifying decisions directory: {str(e)}")
            raise
        
    def analyze_code_impact(self, search_patterns: List[str]) -> Dict:
        """Analyze code impact using grep."""
        results = {
            'files_affected': [],
            'Effected Code Blocks': []
        }
        
        for pattern in search_patterns:
            try:
                # Run grep search
                cmd = ['grep', '-r', pattern, 'src/']
                output = subprocess.check_output(cmd).decode('utf-8')
                
                # Process results
                for line in output.splitlines():
                    if ':' in line:
                        file_path, code = line.split(':', 1)
                        if file_path not in results['files_affected']:
                            results['files_affected'].append(file_path)
                        results['Effected Code Blocks'].append({
                            'file': file_path,
                            'code': code.strip()
                        })
            except subprocess.CalledProcessError:
                print(f"No matches found for pattern: {pattern}")
                
        return results
        
    def create_decision_record(
        self,
        title: str,
        context: str,
        search_patterns: List[str],
        options: List[Dict],
        decision: str,
        rationale: List[str],
        next_steps: List[str],
        status: str = "Undecided",
        decision_type: str = "Technical",
        priority: str = "Medium",
        dependencies: List[str] = None,
        tags: List[str] = None
    ) -> str:
        """Create a decision record with automated code analysis."""
        # Analyze code impact
        impact = self.analyze_code_impact(search_patterns)
        
        # Create decision record
        creation_date = datetime.now().strftime("%Y%m%d")
        decision_data = {
            "Decision": title,
            "Creation Date": creation_date,
            "Status": status,
            "Status History": [
                {
                    "status": status,
                    "date": creation_date,
                    "note": "Initial status"
                }
            ],
            "Type": decision_type,
            "Priority": priority,
            "Context": context,
            "Code Analysis": {
                "Files Affected": impact['files_affected'],
                "Effected Code Blocks": impact['Effected Code Blocks']
            },
            "Options": options,
            "Decision": decision,
            "Decision History": [
                {
                    "decision": decision,
                    "date": creation_date,
                    "note": "Initial decision"
                }
            ],
            "Rationale": rationale,
            "Next Steps": next_steps,
            "Dependencies": dependencies or [],
            "Tags": tags or []
        }
        
        # Generate filename
        filename = f"decision_{creation_date}_{datetime.now().strftime('%H%M%S')}.json"
        filepath = os.path.join(self.decisions_dir, filename)
        
        # Write to file with proper permissions
        try:
            with open(filepath, 'w') as f:
                json.dump(decision_data, f, indent=2)
            
            # Set file permissions (644)
            os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            
            # Verify file exists and is readable
            if not os.path.exists(filepath):
                raise PermissionError(f"Failed to create file: {filepath}")
            if not os.access(filepath, os.R_OK):
                raise PermissionError(f"File not readable: {filepath}")
                
            print(f"Decision record created with proper permissions: {filepath}")
        except Exception as e:
            print(f"Error creating decision record: {str(e)}")
            raise
            
        return filepath
        
    def update_decision_status(self, decision_file: str, new_status: str, note: str = None):
        """Update the status of a decision and record the change."""
        try:
            # Verify file exists and is readable
            if not os.path.exists(decision_file):
                raise FileNotFoundError(f"Decision file not found: {decision_file}")
            if not os.access(decision_file, os.R_OK):
                raise PermissionError(f"Decision file not readable: {decision_file}")
                
            # Read current decision
            with open(decision_file, 'r') as f:
                decision_data = json.load(f)
                
            # Update status
            current_status = decision_data.get("Status")
            if current_status == new_status:
                print(f"Status already set to {new_status}")
                return
                
            # Add status change to history
            change_date = datetime.now().strftime("%Y%m%d")
            status_history = decision_data.get("Status History", [])
            status_history.append({
                "status": new_status,
                "date": change_date,
                "note": note or f"Changed from {current_status} to {new_status}"
            })
            
            # Update decision data
            decision_data["Status"] = new_status
            decision_data["Status History"] = status_history
            
            # Make file writable temporarily
            os.chmod(decision_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            
            # Write updated decision
            with open(decision_file, 'w') as f:
                json.dump(decision_data, f, indent=2)
                
            # Reset file permissions (644)
            os.chmod(decision_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            
            print(f"Decision status updated to {new_status}")
        except Exception as e:
            print(f"Error updating decision status: {str(e)}")
            raise
            
    def update_decision(self, decision_file: str, new_decision: str, note: str = None):
        """Update the decision and record the change."""
        try:
            # Verify file exists and is readable
            if not os.path.exists(decision_file):
                raise FileNotFoundError(f"Decision file not found: {decision_file}")
            if not os.access(decision_file, os.R_OK):
                raise PermissionError(f"Decision file not readable: {decision_file}")
                
            # Read current decision
            with open(decision_file, 'r') as f:
                decision_data = json.load(f)
                
            # Update decision
            current_decision = decision_data.get("Decision")
            if current_decision == new_decision:
                print(f"Decision already set to {new_decision}")
                return
                
            # Add decision change to history
            change_date = datetime.now().strftime("%Y%m%d")
            decision_history = decision_data.get("Decision History", [])
            decision_history.append({
                "decision": new_decision,
                "date": change_date,
                "note": note or f"Changed from previous decision"
            })
            
            # Update decision data
            decision_data["Decision"] = new_decision
            decision_data["Decision History"] = decision_history
            
            # Make file writable temporarily
            os.chmod(decision_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            
            # Write updated decision
            with open(decision_file, 'w') as f:
                json.dump(decision_data, f, indent=2)
                
            # Reset file permissions (644)
            os.chmod(decision_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            
            print(f"Decision updated successfully")
        except Exception as e:
            print(f"Error updating decision: {str(e)}")
            raise

def main():
    """Command line interface for decision recorder."""
    if len(sys.argv) < 2:
        print("Usage: python decision_recorder.py <project_name> [update_status|update_decision] [decision_file] [new_value] [note]")
        sys.exit(1)
        
    project_name = sys.argv[1]
    recorder = DecisionRecorder(project_name)
    
    # Check if this is an update operation
    if len(sys.argv) > 2 and sys.argv[2] in ["update_status", "update_decision"]:
        if len(sys.argv) < 5:
            print("Usage for updates: python decision_recorder.py <project_name> update_status|update_decision <decision_file> <new_value> [note]")
            sys.exit(1)
            
        operation = sys.argv[2]
        decision_file = sys.argv[3]
        new_value = sys.argv[4]
        note = sys.argv[5] if len(sys.argv) > 5 else None
        
        if operation == "update_status":
            recorder.update_decision_status(decision_file, new_value, note)
        elif operation == "update_decision":
            recorder.update_decision(decision_file, new_value, note)
        return
    
    # Create new decision
    title = input("Decision title: ")
    context = input("Context: ")
    search_patterns = input("Search patterns (comma-separated): ").split(',')
    status = input("Status (Decided/Undecided): ")
    
    # Get options
    options = []
    while True:
        option = input("Option (or press Enter to finish): ")
        if not option:
            break
        pros = input("Pros (comma-separated): ").split(',')
        cons = input("Cons (comma-separated): ").split(',')
        options.append({
            "description": option,
            "pros": pros,
            "cons": cons
        })
    
    decision = input("Decision: ")
    rationale = input("Rationale (comma-separated): ").split(',')
    next_steps = input("Next steps (comma-separated): ").split(',')
    
    # Create decision record
    filepath = recorder.create_decision_record(
        title=title,
        context=context,
        search_patterns=search_patterns,
        options=options,
        decision=decision,
        rationale=rationale,
        next_steps=next_steps,
        status=status
    )
    
    print(f"Decision record created: {filepath}")

if __name__ == "__main__":
    main() 