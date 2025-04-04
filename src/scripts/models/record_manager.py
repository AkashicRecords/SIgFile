import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
import logging
from .decision_analyzer import DecisionAnalyzer

@dataclass
class RecordEntry:
    """Base class for all record entries."""
    timestamp: str
    author: str
    type: str
    content: Dict
    related_files: List[str] = None
    tags: List[str] = None

class RecordManager:
    """Manages automated creation and updating of project records."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.analyzer = DecisionAnalyzer()
        self.logger = logging.getLogger(__name__)
        
        # Define record directories
        self.directories = {
            'decisions': self.project_root / 'decisions',
            'changes': self.project_root / 'changes',
            'debug': self.project_root / 'debug',
            'handoff': self.project_root / 'handoff'
        }
        
        # Ensure directories exist
        for dir_path in self.directories.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()
    
    def _generate_record_id(self, prefix: str) -> str:
        """Generate a unique record ID."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefix}_{timestamp}"
    
    def _load_record(self, file_path: Path) -> Dict:
        """Load a record file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'entries': []}
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in {file_path}")
            return {'entries': []}
    
    def _save_record(self, file_path: Path, data: Dict) -> None:
        """Save a record file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving {file_path}: {str(e)}")
    
    def add_entry(self, 
                 record_type: str, 
                 content: Dict, 
                 author: str,
                 related_files: Optional[List[str]] = None,
                 tags: Optional[List[str]] = None) -> str:
        """Add a new entry to a record."""
        entry = RecordEntry(
            timestamp=self._get_timestamp(),
            author=author,
            type=record_type,
            content=content,
            related_files=related_files or [],
            tags=tags or []
        )
        
        # Determine target file based on type
        if record_type == 'decision':
            file_path = self.directories['decisions'] / f"{self._generate_record_id('decision')}.json"
        elif record_type == 'change':
            file_path = self.directories['changes'] / f"{self._generate_record_id('change')}.json"
        elif record_type == 'debug':
            file_path = self.directories['debug'] / f"{self._generate_record_id('debug')}.json"
        else:
            file_path = self.directories['handoff'] / f"{self._generate_record_id('handoff')}.json"
        
        # Load existing record or create new
        record = self._load_record(file_path)
        if 'entries' not in record:
            record['entries'] = []
        
        # Add new entry
        record['entries'].append(asdict(entry))
        
        # Save updated record
        self._save_record(file_path, record)
        
        return str(file_path)
    
    def analyze_decision(self, decision_file: str) -> Dict:
        """Analyze a decision file and return affected files."""
        try:
            analysis = self.analyzer.analyze_decision_file(decision_file)
            return {
                'affected_files': [f.path for f in analysis.affected_files.new_files + 
                                 analysis.affected_files.modified_files + 
                                 analysis.affected_files.deleted_files],
                'files_of_interest': analysis.files_of_interest,
                'implementation_files': analysis.implementation_files
            }
        except Exception as e:
            self.logger.error(f"Error analyzing decision: {str(e)}")
            return {}
    
    def create_decision_record(self, 
                             title: str, 
                             context: str, 
                             decision: str, 
                             author: str,
                             related_files: Optional[List[str]] = None) -> str:
        """Create a new decision record."""
        content = {
            'title': title,
            'context': context,
            'decision': decision,
            'status': 'draft',
            'implementation_status': 'pending'
        }
        
        return self.add_entry(
            record_type='decision',
            content=content,
            author=author,
            related_files=related_files,
            tags=['decision', 'planning']
        )
    
    def create_change_record(self,
                           description: str,
                           author: str,
                           files: List[str],
                           changes: Dict[str, str]) -> str:
        """Create a new change record."""
        content = {
            'description': description,
            'changes': changes,
            'verification_status': 'pending'
        }
        
        return self.add_entry(
            record_type='change',
            content=content,
            author=author,
            related_files=files,
            tags=['change', 'implementation']
        )
    
    def create_debug_record(self,
                          issue: str,
                          author: str,
                          solution: str,
                          related_files: Optional[List[str]] = None) -> str:
        """Create a new debug record."""
        content = {
            'issue': issue,
            'solution': solution,
            'status': 'resolved'
        }
        
        return self.add_entry(
            record_type='debug',
            content=content,
            author=author,
            related_files=related_files,
            tags=['debug', 'issue']
        )
    
    def update_record(self, 
                     file_path: str, 
                     update_type: str, 
                     content: Dict, 
                     author: str) -> None:
        """Update an existing record with new information."""
        path = Path(file_path)
        if not path.exists():
            self.logger.error(f"Record file not found: {file_path}")
            return
        
        record = self._load_record(path)
        if 'entries' not in record:
            record['entries'] = []
        
        entry = RecordEntry(
            timestamp=self._get_timestamp(),
            author=author,
            type=update_type,
            content=content
        )
        
        record['entries'].append(asdict(entry))
        self._save_record(path, record) 