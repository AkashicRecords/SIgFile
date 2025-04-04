import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent
import logging
import hashlib
from .record_format import RecordFormat

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.logger = logging.getLogger('file_watcher')

    def _get_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file contents."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating file hash: {e}")
            return ""

    def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get file metadata."""
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'hash': self._get_file_hash(file_path)
            }
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return {}

    def on_modified(self, event):
        if not event.is_directory:
            record = RecordFormat.create_record(
                record_type='file_change',
                title=f"File Modified: {os.path.basename(event.src_path)}",
                description=f"File {event.src_path} was modified",
                files=[event.src_path],
                metadata={'change_type': 'modified'},
                context={'file_info': self._get_file_info(event.src_path)}
            )
            self.callback(record)

    def on_created(self, event):
        if not event.is_directory:
            record = RecordFormat.create_record(
                record_type='file_change',
                title=f"File Created: {os.path.basename(event.src_path)}",
                description=f"File {event.src_path} was created",
                files=[event.src_path],
                metadata={'change_type': 'created'},
                context={'file_info': self._get_file_info(event.src_path)}
            )
            self.callback(record)

    def on_deleted(self, event):
        if not event.is_directory:
            record = RecordFormat.create_record(
                record_type='file_change',
                title=f"File Deleted: {os.path.basename(event.src_path)}",
                description=f"File {event.src_path} was deleted",
                files=[event.src_path],
                metadata={'change_type': 'deleted'}
            )
            self.callback(record)

class FileWatcher:
    def __init__(self, paths=None, ignore_patterns=None, enable_ai_features=True):
        """Initialize the file watcher with paths and ignore patterns."""
        self.paths = paths or ['.']  # Default to current directory if no paths provided
        self.ignore_patterns = ignore_patterns or [
            '*.code-workspace',
            '*.sublime-*',
            '.idea/*',  # Note the correct pattern for IntelliJ files
            '.git/*',
            '__pycache__/*',
            '*.pyc'
        ]
        self.enable_ai_features = enable_ai_features
        self.logger = logging.getLogger('track_change')
        
        # Setup logging
        self.logger.setLevel(logging.INFO)
        
        # Initialize observer
        self.observer = Observer()
        self.changes = []
        self.change_history = []
        
        # Setup event handler
        self.event_handler = FileChangeHandler(self._handle_change)
        
        # Start watching paths
        for path in self.paths:
            if path.exists():
                self.observer.schedule(self.event_handler, str(path), recursive=True)
                self.logger.info(f"Watching path: {path}")
            else:
                self.logger.warning(f"Path does not exist: {path}")

    def _handle_change(self, file_path, change_type):
        """Handle a file change event."""
        try:
            # Create metadata for the change
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'change_type': change_type,
                'file_path': file_path
            }
            
            # Add AI-specific metadata if enabled
            if self.enable_ai_features:
                metadata['ai_enabled'] = True
                metadata['ide_info'] = self._detect_ide()
            
            # Create backup of the file
            create_backup(file_path, PROJECT_NAME)
            
            # Record the change
            record = {
                'file': file_path,
                'type': change_type,
                'metadata': metadata
            }
            
            return record
            
        except Exception as e:
            self.logger.error(f"Error handling file change: {str(e)}", exc_info=True)
            raise

    def _detect_ide(self):
        """Detect the current IDE environment."""
        # Check for common IDE-specific files and environment variables
        if os.path.exists('.idea'):
            return 'intellij'
        elif os.path.exists('.vscode'):
            return 'vscode'
        elif os.environ.get('SUBLIMINAL_ENVIRONMENT'):
            return 'sublime'
        return 'unknown'

    def _should_ignore(self, file_path):
        """Check if a file should be ignored based on patterns."""
        from fnmatch import fnmatch
        return any(fnmatch(file_path, pattern) for pattern in self.ignore_patterns)

    def watch(self):
        """Watch for file changes in the specified paths."""
        try:
            for path in self.paths:
                if os.path.exists(path):
                    for root, _, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if not self._should_ignore(file_path):
                                # Check if file has been modified
                                if self._is_modified(file_path):
                                    self._handle_change(file_path, 'modified')
        except Exception as e:
            self.logger.error(f"Error watching files: {str(e)}", exc_info=True)
            raise

    def _is_modified(self, file_path):
        """Check if a file has been modified since last check."""
        try:
            current_mtime = os.path.getmtime(file_path)
            if not hasattr(self, '_last_check'):
                self._last_check = {}
            
            if file_path not in self._last_check:
                self._last_check[file_path] = current_mtime
                return False
                
            if current_mtime > self._last_check[file_path]:
                self._last_check[file_path] = current_mtime
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking file modification: {str(e)}", exc_info=True)
            return False

    def start(self) -> None:
        """Start watching for changes."""
        self.observer.start()
        self.logger.info("File watcher started")

    def stop(self) -> None:
        """Stop watching for changes."""
        self.observer.stop()
        self.observer.join()
        self.logger.info("File watcher stopped")

    def get_changes(self) -> List[Dict]:
        """Get list of changes since last check."""
        changes = self.changes.copy()
        self.changes = []
        return changes

    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get change history, optionally limited to a specific number of entries."""
        if limit:
            return self.change_history[-limit:]
        return self.change_history.copy()

    def export_changes(self, format: str = 'json') -> str:
        """Export changes in standardized format."""
        return RecordFormat.export_records(
            self.change_history,
            'file_change',
            {'watched_paths': [str(p) for p in self.paths]}
        )

    def watch(self) -> Optional[Dict]:
        """Watch for a single change and return it."""
        if self.changes:
            return self.changes.pop(0)
        return None

    def is_watching(self) -> bool:
        """Check if the watcher is active."""
        return self.observer.is_alive() 