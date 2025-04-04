from models.record_manager import RecordManager
import logging

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def automated_workflow(project_root: str, author: str):
    """Example of automated record creation workflow."""
    manager = RecordManager(project_root)
    
    # 1. Create decision record for CLI dogfooding
    decision_path = manager.create_decision_record(
        title="CLI Dogfooding Strategy",
        context="Need to validate CLI functionality through self-use",
        decision="Use CLI tool itself for recording changes and decisions",
        author=author,
        related_files=["src/scripts/cli.py"]
    )
    print(f"Created decision record: {decision_path}")
    
    # 2. Create change record for decision analyzer
    change_path = manager.create_change_record(
        description="Initial implementation of decision analyzer module",
        author=author,
        files=["src/scripts/models/decision_analyzer.py"],
        changes={
            "decision_analyzer.py": "Added core analyzer functionality"
        }
    )
    print(f"Created change record: {change_path}")
    
    # 3. Create debug record for zombie process prevention
    debug_path = manager.create_debug_record(
        issue="Potential resource leaks in decision analyzer",
        author=author,
        solution="Added context managers and cleanup methods",
        related_files=["src/scripts/models/decision_analyzer.py"]
    )
    print(f"Created debug record: {debug_path}")
    
    # 4. Update decision record with implementation status
    manager.update_record(
        decision_path,
        "implementation_update",
        {
            "status": "implemented",
            "implementation_status": "complete",
            "notes": "Successfully implemented and tested"
        },
        author
    )
    print(f"Updated decision record: {decision_path}")

def manual_workflow(project_root: str, author: str):
    """Example of manual record creation workflow."""
    manager = RecordManager(project_root)
    
    # Example of manual decision analysis
    decision_file = "tracked_projects/sigfile-cli/decisions/006_cursor_proxy_implementation.md"
    analysis = manager.analyze_decision(decision_file)
    
    # Create change record based on analysis
    change_path = manager.create_change_record(
        description="Implementation of Cursor proxy based on decision analysis",
        author=author,
        files=analysis['affected_files'],
        changes={
            file: "Implemented based on decision requirements"
            for file in analysis['affected_files']
        }
    )
    print(f"Created change record from analysis: {change_path}")

def main():
    setup_logging()
    
    # Example usage
    project_root = "tracked_projects/sigfile-cli"
    author = "developer"
    
    try:
        # Run automated workflow
        print("Running automated workflow...")
        automated_workflow(project_root, author)
        
        # Run manual workflow
        print("\nRunning manual workflow...")
        manual_workflow(project_root, author)
        
    except Exception as e:
        logging.error(f"Error in workflow: {str(e)}")

if __name__ == "__main__":
    main() 