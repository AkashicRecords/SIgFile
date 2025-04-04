import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from contextlib import contextmanager
import weakref
import gc
from .affected_files import AffectedFiles, FileChange

@dataclass
class DecisionAnalysis:
    """Results of analyzing a decision record."""
    affected_files: AffectedFiles
    files_of_interest: List[str]  # Files mentioned but not directly affected
    implementation_files: List[str]  # Files mentioned in implementation section
    references: Dict[str, List[str]]  # Files referenced in different sections
    
    def __del__(self):
        """Cleanup method to ensure proper resource release."""
        self.affected_files = None
        self.files_of_interest.clear()
        self.implementation_files.clear()
        self.references.clear()

class DecisionAnalyzer:
    """Analyzes decision records to extract file information."""
    
    def __init__(self):
        self.file_patterns = {
            'new': r'new file[s]?.*?`([^`]+)`',
            'modified': r'modif(?:y|ied).*?`([^`]+)`',
            'deleted': r'delete[d]?.*?`([^`]+)`',
            'implementation': r'implementation.*?`([^`]+)`',
            'reference': r'`([^`]+)`'  # General file references
        }
        self._finalizer = weakref.finalize(self, self._cleanup)
    
    def _cleanup(self):
        """Internal cleanup method."""
        self.file_patterns.clear()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self._cleanup()
        return False  # Don't suppress exceptions
    
    @contextmanager
    def _safe_file_handle(self, file_path: str):
        """Safely handle file operations with cleanup."""
        file_handle = None
        try:
            file_handle = open(file_path, 'r')
            yield file_handle
        finally:
            if file_handle is not None:
                file_handle.close()
    
    def analyze_decision(self, content: str, base_path: Optional[str] = None) -> DecisionAnalysis:
        """Analyze a decision record to extract file information."""
        try:
            affected = AffectedFiles()
            files_of_interest = set()
            implementation_files = set()
            references = {}
            
            # Extract files from different sections
            for section, pattern in self.file_patterns.items():
                try:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    files = [m.group(1) for m in matches]
                    
                    if section == 'new':
                        for file in files:
                            affected.add_new_file(file, "Created as part of decision implementation")
                    elif section == 'modified':
                        for file in files:
                            affected.add_modified_file(file, "Modified as part of decision implementation")
                    elif section == 'deleted':
                        for file in files:
                            affected.add_deleted_file(file, "Removed as part of decision implementation")
                    elif section == 'implementation':
                        implementation_files.update(files)
                    else:
                        files_of_interest.update(files)
                    
                    references[section] = files
                except Exception as e:
                    print(f"Warning: Error processing section {section}: {str(e)}")
                    continue
            
            # Validate paths if base_path is provided
            if base_path:
                try:
                    errors = affected.validate_paths(base_path)
                    if errors:
                        print("Warning: Some files referenced in decision do not exist:")
                        for error in errors:
                            print(f"- {error}")
                except Exception as e:
                    print(f"Warning: Error validating paths: {str(e)}")
            
            return DecisionAnalysis(
                affected_files=affected,
                files_of_interest=list(files_of_interest),
                implementation_files=list(implementation_files),
                references=references
            )
        except Exception as e:
            print(f"Error analyzing decision: {str(e)}")
            raise
    
    def analyze_decision_file(self, file_path: str) -> DecisionAnalysis:
        """Analyze a decision record file to extract file information."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Decision file not found: {file_path}")
        
        try:
            with self._safe_file_handle(str(path)) as f:
                content = f.read()
            return self.analyze_decision(content, str(path.parent))
        except Exception as e:
            print(f"Error analyzing decision file {file_path}: {str(e)}")
            raise
    
    def generate_summary(self, analysis: DecisionAnalysis) -> str:
        """Generate a summary of the analysis results."""
        try:
            summary = []
            
            # Affected files summary
            if analysis.affected_files.new_files or analysis.affected_files.modified_files or analysis.affected_files.deleted_files:
                summary.append("## Affected Files Summary")
                summary.append(analysis.affected_files.to_markdown())
            
            # Files of interest
            if analysis.files_of_interest:
                summary.append("\n## Files of Interest")
                summary.append("Files mentioned in the decision but not directly affected:")
                for file in analysis.files_of_interest:
                    summary.append(f"- `{file}`")
            
            # Implementation files
            if analysis.implementation_files:
                summary.append("\n## Implementation Files")
                summary.append("Files mentioned in the implementation section:")
                for file in analysis.implementation_files:
                    summary.append(f"- `{file}`")
            
            return "\n".join(summary)
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "Error generating summary"
    
    def __del__(self):
        """Ensure cleanup on object destruction."""
        self._cleanup() 