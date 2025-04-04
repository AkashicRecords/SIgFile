from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class FileChange:
    path: str
    description: str
    type: str  # 'new', 'modified', or 'deleted'

class AffectedFiles:
    def __init__(self):
        self.new_files: List[FileChange] = []
        self.modified_files: List[FileChange] = []
        self.deleted_files: List[FileChange] = []

    def add_new_file(self, path: str, purpose: str) -> None:
        """Add a new file to the affected files list."""
        self.new_files.append(FileChange(path=path, description=purpose, type='new'))

    def add_modified_file(self, path: str, changes: str) -> None:
        """Add a modified file to the affected files list."""
        self.modified_files.append(FileChange(path=path, description=changes, type='modified'))

    def add_deleted_file(self, path: str, reason: str) -> None:
        """Add a deleted file to the affected files list."""
        self.deleted_files.append(FileChange(path=path, description=reason, type='deleted'))

    def to_markdown(self) -> str:
        """Convert the affected files to markdown format."""
        markdown = "## Affected Files\n"
        
        if self.new_files:
            markdown += "\n### New Files\n"
            for file in self.new_files:
                markdown += f"- `{file.path}`: {file.description}\n"
        
        if self.modified_files:
            markdown += "\n### Modified Files\n"
            for file in self.modified_files:
                markdown += f"- `{file.path}`: {file.description}\n"
        
        if self.deleted_files:
            markdown += "\n### Deleted Files\n"
            for file in self.deleted_files:
                markdown += f"- `{file.path}`: {file.description}\n"
        
        return markdown

    def to_yaml(self) -> str:
        """Convert the affected files to YAML format."""
        yaml = "affected_files:\n"
        
        if self.new_files:
            yaml += "  new_files:\n"
            for file in self.new_files:
                yaml += f"    - path: {file.path}\n"
                yaml += f"      purpose: {file.description}\n"
        
        if self.modified_files:
            yaml += "  modified_files:\n"
            for file in self.modified_files:
                yaml += f"    - path: {file.path}\n"
                yaml += f"      changes: {file.description}\n"
        
        if self.deleted_files:
            yaml += "  deleted_files:\n"
            for file in self.deleted_files:
                yaml += f"    - path: {file.path}\n"
                yaml += f"      reason: {file.description}\n"
        
        return yaml

    def validate_paths(self, base_path: Optional[str] = None) -> List[str]:
        """Validate that all file paths exist (except for deleted files)."""
        errors = []
        base = Path(base_path) if base_path else Path.cwd()
        
        for file in self.new_files + self.modified_files:
            full_path = base / file.path
            if not full_path.exists():
                errors.append(f"File does not exist: {file.path}")
        
        return errors 