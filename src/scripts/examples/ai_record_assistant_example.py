import asyncio
import logging
from models.record_manager import RecordManager
from models.ai_record_assistant import AIRecordAssistant

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

async def create_records_with_ai(project_root: str, author: str):
    """Example of creating records with AI assistance."""
    manager = RecordManager(project_root)
    assistant = AIRecordAssistant(manager)
    
    try:
        # 1. Create a decision record with AI assistance
        print("Creating decision record with AI assistance...")
        decision_path = await assistant.create_decision_record_with_ai(author)
        print(f"Created decision record: {decision_path}")
        
        # 2. Create a change record with AI assistance
        print("\nCreating change record with AI assistance...")
        change_path = await assistant.create_change_record_with_ai(
            files=["src/scripts/models/ai_record_assistant.py"],
            author=author
        )
        print(f"Created change record: {change_path}")
        
        # 3. Create a debug record with AI assistance
        print("\nCreating debug record with AI assistance...")
        debug_path = await assistant.create_debug_record_with_ai(
            issue="Potential issues with AI response parsing",
            author=author
        )
        print(f"Created debug record: {debug_path}")
        
    except Exception as e:
        logging.error(f"Error creating records: {str(e)}")

def main():
    setup_logging()
    
    # Example usage
    project_root = "tracked_projects/sigfile-cli"
    author = "developer"
    
    # Run the async function
    asyncio.run(create_records_with_ai(project_root, author))

if __name__ == "__main__":
    main() 