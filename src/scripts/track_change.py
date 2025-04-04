#!/usr/bin/env python3

import os
import sys
import argparse
from datetime import datetime, timedelta
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import json
import logging
import threading
import queue
import time
import shutil
import gzip
import stat
from .permission_manager import permission_manager
from enum import Enum

# Configure logging for development
def setup_logging():
    """Set up logging configuration for development."""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger('sigfile')
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    logger.handlers = []

    # Console handler with color formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler for detailed logs
    log_file = os.path.join(logs_dir, 'track_change.log')
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

# Initialize logger
logger = setup_logging()

# Import AI tracking modules
try:
    from . import ai_tracking
    from . import decision_tracking
    from . import file_watcher
except ImportError:
    import ai_tracking
    import decision_tracking
    import file_watcher

AITracking = ai_tracking.AITracking
DecisionTracker = decision_tracking.DecisionTracker
FileWatcher = file_watcher.FileWatcher

# Configuration
SIGFILE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_NAME = "logiclens"  # Default project, can be overridden with -p flag

# Archive configuration
ARCHIVE_CONFIG = {
    'size_threshold_mb': 100,  # Archive files larger than 100MB
    'age_threshold_days': 30,  # Archive files older than 30 days
    'check_interval_hours': 24,  # Check for archiving every 24 hours
    'compression_level': 6      # GZIP compression level (1-9)
}

class FileRole(Enum):
    """Enum representing different file access roles."""
    SYSTEM = "SYSTEM"
    AI_AGENT = "AI_AGENT"
    ADMIN = "ADMIN"
    USER = "USER"

def get_config_dirs(project_name):
    """Get configuration directories for the specified project."""
    if not project_name:
        logger.error("Project name cannot be empty")
        raise ValueError("Project name cannot be empty")
        
    try:
        # Use root tracked_projects directory
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'tracked_projects', project_name)
        dirs = {
            'logs': os.path.join(base_dir, 'logs'),
            'changes': os.path.join(base_dir, 'changes'),
            'backups': os.path.join(base_dir, 'backups'),
            'ai_conversations': os.path.join(base_dir, 'ai_conversations'),
            'thinking': os.path.join(base_dir, 'thinking'),
            'handoffs': os.path.join(base_dir, 'handoffs')
        }
        
        # Create directories if they don't exist
        for dir_path in dirs.values():
            os.makedirs(dir_path, exist_ok=True)
            logger.debug(f"Created directory: {dir_path}")
            
        return dirs
    except Exception as e:
        logger.error(f"Error creating configuration directories: {str(e)}")
        raise

def get_timestamp():
    """Get current timestamp in YYYYMMDD_HHMMSS_MMMMMM format."""
    try:
        now = datetime.now()
        # Ensure we're using the correct year
        if now.year != 2024:
            logger.warning(f"System year is {now.year}, adjusting to 2024")
            now = now.replace(year=2024)
        return now.strftime('%Y%m%d_%H%M%S_%f')
    except Exception as e:
        logger.error(f"Error generating timestamp: {str(e)}")
        raise

def log(message):
    """Log message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def make_immutable(file_path):
    """Make a file immutable."""
    logger.debug(f"Attempting to make {file_path} immutable")
    try:
        current_mode = os.stat(file_path).st_mode
        logger.debug(f"Current file mode: {current_mode}")
        
        # Remove write permissions
        new_mode = stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH
        logger.debug(f"New file mode: {new_mode}")
        
        os.chmod(file_path, new_mode)
        logger.debug(f"Successfully changed file mode")
    except Exception as e:
        logger.error(f"Error in _make_immutable: {str(e)}")
        raise

def make_mutable(file_path):
    """Make a file mutable by setting it to read-write."""
    try:
        # Set file to read-write for owner (0o644)
        os.chmod(file_path, 0o644)
        logger.debug(f"Made file mutable: {file_path}")
    except Exception as e:
        logger.error(f"Error making file mutable: {str(e)}")
        raise

def create_backup(file_path, project_name):
    """Create a backup of the specified file."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        dirs = get_config_dirs(project_name)
        timestamp = get_timestamp()
        backup_dir = os.path.join(dirs['backups'], timestamp[:8])
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_path = os.path.join(backup_dir, f"{os.path.basename(file_path)}_{timestamp}")
        shutil.copy2(file_path, backup_path)
        # Make backup immutable since it won't be modified
        make_immutable(backup_path)
        logger.info(f"Created backup: {backup_path}")
        
    except Exception as e:
        logger.error(f"Error creating backup: {str(e)}")
        raise

def record_change(description, files_changed, project_name):
    """Record a change with description and files changed.
    
    Returns:
        str: Path to the created change file
    """
    if not description or not files_changed:
        logger.error("Description and files changed are required")
        raise ValueError("Description and files changed are required")
        
    try:
        dirs = get_config_dirs(project_name)
        timestamp = get_timestamp()
        changes_dir = os.path.join(dirs['changes'], timestamp[:8])
        os.makedirs(changes_dir, exist_ok=True)
        
        change_file = os.path.join(changes_dir, f"change_{timestamp}.txt")
        with open(change_file, 'w') as f:
            f.write(f"Description: {description}\n")
            f.write(f"Files Changed: {files_changed}\n")
            f.write(f"Timestamp: {timestamp}\n")
            
        # Change files remain mutable until explicitly marked as complete
        logger.info(f"Recorded change: {change_file}")
        return change_file
        
    except Exception as e:
        logger.error(f"Error recording change: {str(e)}")
        raise

def finalize_change(change_file):
    """Mark a change file as complete by making it immutable."""
    try:
        if os.path.exists(change_file):
            make_immutable(change_file)
            logger.info(f"Finalized change file: {change_file}")
        else:
            logger.error(f"Change file not found: {change_file}")
            raise FileNotFoundError(f"Change file not found: {change_file}")
    except Exception as e:
        logger.error(f"Error finalizing change: {str(e)}")
        raise

def show_history(date, project_name):
    """Show change history for the specified date."""
    try:
        dirs = get_config_dirs(project_name)
        changes = []
        
        if date:
            # If a specific date is provided, look in that date's directory
            date_dir = os.path.join(dirs['changes'], date)
            if os.path.exists(date_dir):
                for item in os.listdir(date_dir):
                    if item.endswith('.txt') and item.startswith('change_'):
                        item_path = os.path.join(date_dir, item)
                        if os.path.isfile(item_path):
                            with open(item_path, 'r') as f:
                                content = f.read()
                                changes.append(content)
            else:
                logger.warning(f"No changes found for date: {date}")
        else:
            # If no date is provided, look in all date directories
            for date_dir in os.listdir(dirs['changes']):
                date_path = os.path.join(dirs['changes'], date_dir)
                if os.path.isdir(date_path):
                    for item in os.listdir(date_path):
                        if item.endswith('.txt') and item.startswith('change_'):
                            item_path = os.path.join(date_path, item)
                            if os.path.isfile(item_path):
                                with open(item_path, 'r') as f:
                                    content = f.read()
                                    changes.append(content)
        
        logger.info(f"Retrieved {len(changes)} changes from history")
        return changes
    except Exception as e:
        logger.error(f"Error showing history: {str(e)}")
        raise

def generate_handoff(chat_name, chat_id, summary, next_steps, project_name):
    """Generate a handoff document."""
    if not all([chat_name, chat_id, summary, next_steps]):
        logger.error("All handoff fields are required")
        raise ValueError("All handoff fields are required")
        
    try:
        dirs = get_config_dirs(project_name)
        timestamp = get_timestamp()
        handoffs_dir = os.path.join(dirs['handoffs'], timestamp[:8])
        os.makedirs(handoffs_dir, exist_ok=True)
        
        handoff_file = os.path.join(handoffs_dir, f"handoff_{timestamp}.txt")
        with open(handoff_file, 'w') as f:
            f.write(f"Chat Name: {chat_name}\n")
            f.write(f"Chat ID: {chat_id}\n")
            f.write(f"Summary: {summary}\n")
            f.write(f"Next Steps: {next_steps}\n")
            f.write(f"Timestamp: {timestamp}\n")
        
        # Make handoff immutable since it won't be modified
        make_immutable(handoff_file)
        logger.info(f"Generated handoff: {handoff_file}")
        
    except Exception as e:
        logger.error(f"Error generating handoff: {str(e)}")
        raise

def setup():
    """Set up SigFile environment."""
    # Check for moreutils
    try:
        subprocess.run(['ts', '--version'], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        log("Installing moreutils...")
        try:
            subprocess.run(['brew', 'install', 'moreutils'], check=True)
        except subprocess.CalledProcessError:
            log("ERROR: Homebrew not found. Please install moreutils manually.")
            sys.exit(1)
    
    # Create directory structure
    for dir_name in ['config/settings', 'config/backups', 'config/changes', 'config/handoffs', 'src/scripts', 'src/templates']:
        os.makedirs(os.path.join(SIGFILE_DIR, dir_name), exist_ok=True)
    
    # Make CLI executable
    cli_path = os.path.join(SIGFILE_DIR, 'src', 'scripts', 'cli.py')
    if os.path.exists(cli_path):
        os.chmod(cli_path, 0o755)
        log("Made CLI executable")
    
    # Create symlink for easy access
    try:
        symlink_path = os.path.join(SIGFILE_DIR, 'sigfile')
        if not os.path.exists(symlink_path):
            os.symlink(cli_path, symlink_path)
            log("Created symlink for easy access")
    except Exception as e:
        log(f"Warning: Could not create symlink: {e}")
    
    log("SigFile setup complete!")

def should_archive_file(file_path: str) -> bool:
    """
    Determine if a file should be archived based on size and age.
    """
    try:
        if not os.path.exists(file_path):
            return False
            
        # Check file size
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > ARCHIVE_CONFIG['size_threshold_mb']:
            logger.info(f"File {file_path} exceeds size threshold ({size_mb:.2f}MB)")
            return True
            
        # Check file age
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        age_days = (datetime.now() - mtime).days
        if age_days > ARCHIVE_CONFIG['age_threshold_days']:
            logger.info(f"File {file_path} exceeds age threshold ({age_days} days)")
            return True
            
        return False
    except Exception as e:
        logger.error(f"Error checking archive status: {str(e)}")
        return False

def archive_file(file_path: str) -> str:
    """
    Archive a file using gzip compression and return the archive path.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Create archive directory if it doesn't exist
        archive_dir = os.path.join(os.path.dirname(file_path), 'archive')
        os.makedirs(archive_dir, exist_ok=True)
        
        # Generate archive path with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_path = os.path.join(archive_dir, f"{os.path.basename(file_path)}_{timestamp}.gz")
        
        # Compress file
        with open(file_path, 'rb') as f_in:
            with gzip.open(archive_path, 'wb', compresslevel=ARCHIVE_CONFIG['compression_level']) as f_out:
                shutil.copyfileobj(f_in, f_out)
                
        # Create metadata file
        metadata = {
            'original_path': file_path,
            'archive_date': timestamp,
            'original_size': os.path.getsize(file_path),
            'compressed_size': os.path.getsize(archive_path)
        }
        metadata_path = archive_path + '.meta'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        # Make both files immutable
        make_immutable(archive_path)
        make_immutable(metadata_path)
        
        logger.info(f"Archived file {file_path} to {archive_path}")
        return archive_path
        
    except Exception as e:
        logger.error(f"Error archiving file: {str(e)}")
        raise

def check_and_archive_directory(directory: str):
    """
    Check all files in a directory and its subdirectories for archiving.
    """
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.gz') or file.endswith('.meta'):
                    continue
                    
                file_path = os.path.join(root, file)
                if should_archive_file(file_path):
                    archive_file(file_path)
                    
    except Exception as e:
        logger.error(f"Error checking directory for archiving: {str(e)}")
        raise

class ArchiveManager:
    """Manages the archiving of files based on configured thresholds."""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.dirs = get_config_dirs(project_name)
        self.last_check = None
        
    def should_check_archives(self) -> bool:
        """Determine if it's time to check for archiving."""
        if not self.last_check:
            return True
            
        hours_since_check = (datetime.now() - self.last_check).total_seconds() / 3600
        return hours_since_check >= ARCHIVE_CONFIG['check_interval_hours']
        
    def run_archive_check(self):
        """Check and archive files if necessary."""
        try:
            if not self.should_check_archives():
                return
                
            logger.info("Starting archive check...")
            for dir_path in self.dirs.values():
                check_and_archive_directory(dir_path)
                
            self.last_check = datetime.now()
            logger.info("Archive check completed")
            
        except Exception as e:
            logger.error(f"Error during archive check: {str(e)}")
            raise

class OptimizedCapture:
    def __init__(self, project_name: str = "sigfile"):
        """Initialize the OptimizedCapture class."""
        self.project_name = project_name
        self.project_dir = os.path.join('tracked_projects', project_name)
        self.config_dirs = get_config_dirs(project_name)
        self.logger = logger
        self.logger.info(f"Initializing OptimizedCapture for project: {project_name}")
        
        # Initialize file roles dictionary
        self.file_roles = {}
        
        # Set up directories
        self._setup_directories()
        
        # Initialize components
        self._initialize_components()
    
    def _setup_directories(self):
        """Set up project directories."""
        try:
            # Create base project directory
            os.makedirs(self.project_dir, exist_ok=True)
            self.logger.info(f"Created project directory: {self.project_dir}")
            
            # Create subdirectories
            for dir_name in ['changes', 'backups', 'logs', 'ai_conversations', 'thinking']:
                dir_path = os.path.join(self.project_dir, dir_name)
                os.makedirs(dir_path, exist_ok=True)
                self.logger.info(f"Created directory: {dir_path}")
                
        except Exception as e:
            self.logger.error(f"Error setting up directories: {e}")
            raise
    
    def _initialize_components(self):
        """Initialize tracking components."""
        try:
            # Initialize AI tracking
            self.ai_tracker = AITracking(self.project_name)
            self.logger.info("Initialized AI tracking")
            
            # Initialize decision tracking
            self.decision_tracker = DecisionTracker(self.project_name)
            self.logger.info("Initialized decision tracking")
            
            # Initialize file watcher
            self.file_watcher = FileWatcher(self.project_name)
            self.logger.info("Initialized file watcher")
            
        except Exception as e:
            self.logger.error(f"Error initializing components: {e}")
            raise

    def start_capture(self):
        """Start the capture system."""
        try:
            # Start file watcher thread
            self.file_thread = threading.Thread(target=self._file_capture_loop)
            self.file_thread.daemon = True
            self.file_thread.start()
            
            # Start chat capture thread if AI features enabled
            if self.enable_ai_features:
                self.chat_thread = threading.Thread(target=self._chat_capture_loop)
                self.chat_thread.daemon = True
                self.chat_thread.start()
                
                self.thinking_thread = threading.Thread(target=self._thinking_capture_loop)
                self.thinking_thread.daemon = True
                self.thinking_thread.start()
                
            self.logger.info("Capture system started")
            
        except Exception as e:
            self.logger.error(f"Error starting capture system: {str(e)}", exc_info=True)
            raise

    def stop_capture(self):
        """Stop the capture system."""
        try:
            self.stop_event.set()
            if hasattr(self, 'file_thread'):
                self.file_thread.join()
            if hasattr(self, 'chat_thread'):
                self.chat_thread.join()
            if hasattr(self, 'thinking_thread'):
                self.thinking_thread.join()
            self.logger.info("Capture system stopped")
        except Exception as e:
            self.logger.error(f"Error stopping capture system: {str(e)}", exc_info=True)
            raise

    def _file_capture_loop(self):
        """Main loop for file change capture."""
        while not self.stop_event.is_set():
            try:
                if not self.file_queue.empty():
                    change = self.file_queue.get()
                    self._handle_file_change(change)
            except Exception as e:
                self.logger.error(f"Error in file capture: {str(e)}", exc_info=True)
            time.sleep(0.1)

    def _chat_capture_loop(self):
        """Main loop for chat capture."""
        while not self.stop_event.is_set():
            try:
                if not self.chat_queue.empty():
                    message = self.chat_queue.get()
                    self._handle_chat_message(message)
            except Exception as e:
                self.logger.error(f"Error in chat capture: {str(e)}", exc_info=True)
            time.sleep(0.1)

    def _thinking_capture_loop(self):
        """Main loop for thinking capture."""
        while not self.stop_event.is_set():
            try:
                if not self.thinking_queue.empty():
                    thought = self.thinking_queue.get()
                    self._handle_thinking(thought)
            except Exception as e:
                self.logger.error(f"Error in thinking capture: {str(e)}", exc_info=True)
            time.sleep(0.1)

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

    def _handle_file_change(self, change):
        """Handle file change events."""
        try:
            if self.enable_ai_features:
                # Process with AI features
                self.file_queue.put(change)
            else:
                # Process without AI features
                self.logger.info(f"File change detected: {change}")
        except Exception as e:
            self.logger.error(f"Error handling file change: {str(e)}", exc_info=True)
            raise

    def _verify_directory_permissions(self, directory):
        """Verify that all directories are writable."""
        try:
            # Test write permission by creating a temporary file
            test_file = os.path.join(directory, '.permission_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            logger.info(f"Directory permissions verified for {directory}")
        except Exception as e:
            logger.error(f"Directory permission verification failed for {directory}: {str(e)}")
            raise

    def _record_permission_change(self, file_path: str, role: FileRole, action: str, details: str):
        """Record permission changes in the change history."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            changes_dir = os.path.join('tracked_projects', self.project_name, 'changes')
            date_dir = os.path.join(changes_dir, datetime.now().strftime("%Y%m%d"))
            os.makedirs(date_dir, exist_ok=True)
            
            change_file = os.path.join(date_dir, f'changes_{timestamp}.txt')
            
            with open(change_file, 'w') as f:
                f.write(f"# Permission Change Record - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## File: {file_path}\n")
                f.write(f"## Role: {role.value}\n")
                f.write(f"## Action: {action}\n")
                f.write(f"## Details: {details}\n\n")
                f.write("## Context:\n")
                f.write(f"- Current Roles: {[r.value for r in self.file_roles.get(file_path, set())]}\n")
                f.write(f"- Operation: {action}\n")
                f.write(f"- Timestamp: {timestamp}\n")
            
            # Make the change record immutable
            self._make_immutable(change_file)
            
            # Update change history
            history_file = os.path.join(changes_dir, 'change_history.txt')
            with open(history_file, 'a') as f:
                f.write(f"\n## Permission Change - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"1. File: {file_path}\n")
                f.write(f"2. Role: {role.value}\n")
                f.write(f"3. Action: {action}\n")
                f.write(f"4. Details: {details}\n")
            
            self.logger.info(f"Recorded permission change for {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error recording permission change: {str(e)}", exc_info=True)

    def _record_development_decision(self, decision_type: str, description: str, context: str, outcome: str, related_changes: List[str] = None):
        """Record development decisions, attempts, and changes in direction."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            changes_dir = os.path.join('tracked_projects', self.project_name, 'changes')
            date_dir = os.path.join(changes_dir, datetime.now().strftime("%Y%m%d"))
            os.makedirs(date_dir, exist_ok=True)
            
            decision_file = os.path.join(date_dir, f'development_decision_{timestamp}.txt')
            
            with open(decision_file, 'w') as f:
                f.write(f"# Development Decision Record - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## Type: {decision_type}\n")
                f.write(f"## Description: {description}\n")
                f.write(f"## Context: {context}\n")
                f.write(f"## Outcome: {outcome}\n\n")
                f.write("## Related Code Changes:\n")
                if related_changes:
                    for change in related_changes:
                        f.write(f"- {change}\n")
                else:
                    f.write("No direct code changes associated with this decision.\n")
                f.write("\n## Additional Context:\n")
                f.write(f"- Timestamp: {timestamp}\n")
                f.write(f"- Decision ID: {timestamp}\n")
                f.write(f"- Status: {'Implemented' if outcome == 'Success' else 'In Progress'}\n")
            
            # Make the decision record immutable
            self._make_immutable(decision_file)
            
            # Update development history
            history_file = os.path.join(changes_dir, 'development_history.txt')
            with open(history_file, 'a') as f:
                f.write(f"\n## Development Decision - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"1. Type: {decision_type}\n")
                f.write(f"2. Description: {description}\n")
                f.write(f"3. Context: {context}\n")
                f.write(f"4. Outcome: {outcome}\n")
                if related_changes:
                    f.write("5. Related Changes:\n")
                    for change in related_changes:
                        f.write(f"   - {change}\n")
            
            self.logger.info(f"Recorded development decision: {decision_type}")
            
        except Exception as e:
            self.logger.error(f"Error recording development decision: {str(e)}", exc_info=True)

    def _record_code_change(self, file_path: str, change_type: str, description: str, decision_id: str = None):
        """Record a code change and optionally link it to a development decision."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            changes_dir = os.path.join('tracked_projects', self.project_name, 'changes')
            date_dir = os.path.join(changes_dir, datetime.now().strftime("%Y%m%d"))
            os.makedirs(date_dir, exist_ok=True)
            
            change_file = os.path.join(date_dir, f'code_change_{timestamp}.txt')
            
            with open(change_file, 'w') as f:
                f.write(f"# Code Change Record - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## File: {file_path}\n")
                f.write(f"## Type: {change_type}\n")
                f.write(f"## Description: {description}\n")
                if decision_id:
                    f.write(f"## Related Decision: {decision_id}\n")
                f.write("\n## Context:\n")
                f.write(f"- Timestamp: {timestamp}\n")
                f.write(f"- Change ID: {timestamp}\n")
            
            # Make the change record immutable
            self._make_immutable(change_file)
            
            # Update change history
            history_file = os.path.join(changes_dir, 'change_history.txt')
            with open(history_file, 'a') as f:
                f.write(f"\n## Code Change - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"1. File: {file_path}\n")
                f.write(f"2. Type: {change_type}\n")
                f.write(f"3. Description: {description}\n")
                if decision_id:
                    f.write(f"4. Related Decision: {decision_id}\n")
            
            self.logger.info(f"Recorded code change for {file_path}")
            
            return timestamp  # Return the change ID for linking to decisions
            
        except Exception as e:
            self.logger.error(f"Error recording code change: {str(e)}", exc_info=True)
            return None

    def _link_change_to_decision(self, change_id: str, decision_id: str):
        """Link a code change to a development decision."""
        try:
            changes_dir = os.path.join('tracked_projects', self.project_name, 'changes')
            date_dir = os.path.join(changes_dir, datetime.now().strftime("%Y%m%d"))
            
            # Update the change record
            change_file = os.path.join(date_dir, f'code_change_{change_id}.txt')
            if os.path.exists(change_file):
                with open(change_file, 'r') as f:
                    content = f.read()
                
                # Add decision link if not already present
                if "Related Decision:" not in content:
                    with open(change_file, 'w') as f:
                        f.write(content)
                        f.write(f"\n## Related Decision: {decision_id}\n")
            
            # Update the decision record
            decision_file = os.path.join(date_dir, f'development_decision_{decision_id}.txt')
            if os.path.exists(decision_file):
                with open(decision_file, 'r') as f:
                    content = f.read()
                
                # Add change link if not already present
                if f"code_change_{change_id}" not in content:
                    with open(decision_file, 'w') as f:
                        f.write(content)
                        f.write(f"- code_change_{change_id}\n")
            
            self.logger.info(f"Linked change {change_id} to decision {decision_id}")
            
        except Exception as e:
            self.logger.error(f"Error linking change to decision: {str(e)}", exc_info=True)

    def _setup_dev_environment(self):
        """Set up development environment permissions."""
        try:
            # Create a development environment file
            dev_env_file = os.path.join(self.project_dir, '.dev_environment')
            
            # Check if development environment file exists
            if not os.path.exists(dev_env_file):
                # Create development environment file
                with open(dev_env_file, 'w') as f:
                    f.write(f"Development environment for {self.project_name}\n")
                    f.write(f"Created: {get_timestamp()}\n")
                
                # Make the file immutable
                self._make_immutable(dev_env_file)
                
                self.logger.info("Development environment file created")
            
            # Grant development role access to all files
            for root, _, files in os.walk(self.project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Skip the development environment file
                    if file_path == dev_env_file:
                        continue
                    
                    # Make files writable for development
                    try:
                        # Remove immutable flags
                        if sys.platform == 'linux':
                            subprocess.run(['chattr', '-i', file_path], check=True)
                        elif sys.platform == 'darwin':
                            subprocess.run(['chflags', 'nouchg', file_path], check=True)
                        elif sys.platform == 'win32':
                            subprocess.run(['attrib', '-R', '-S', '-H', file_path], check=True)
                        
                        # Set writable permissions
                        os.chmod(file_path, stat.S_IREAD | stat.S_IWRITE | stat.S_IRGRP | stat.S_IWGRP)
                        
                        self.logger.info(f"Made file writable for development: {file_path}")
                    except Exception as e:
                        self.logger.warning(f"Could not make file writable for development: {file_path}, error: {str(e)}")
            
            self.logger.info("Development environment permissions set up successfully")
            
        except Exception as e:
            self.logger.error(f"Error setting up development environment permissions: {str(e)}", exc_info=True)
            raise
    
    def enable_dev_mode(self, file_path: str = None):
        """Enable development mode for a specific file or all files."""
        try:
            if file_path:
                # Enable development mode for a specific file
                permission_manager.enable_dev_mode(file_path)
                self.logger.info(f"Development mode enabled for file: {file_path}")
            else:
                # Enable development mode for all files
                permission_manager.enable_dev_mode()
                self.logger.info("Development mode enabled for all files")
        except Exception as e:
            self.logger.error(f"Error enabling development mode: {str(e)}", exc_info=True)
            raise
    
    def disable_dev_mode(self, file_path: str = None):
        """Disable development mode for a specific file or all files."""
        try:
            if file_path:
                # Disable development mode for a specific file
                permission_manager.disable_dev_mode(file_path)
                self.logger.info(f"Development mode disabled for file: {file_path}")
            else:
                # Disable development mode for all files
                permission_manager.disable_dev_mode()
                self.logger.info("Development mode disabled for all files")
        except Exception as e:
            self.logger.error(f"Error disabling development mode: {str(e)}", exc_info=True)
            raise

def main():
    """Main entry point for SigFile."""
    parser = argparse.ArgumentParser(description='SigFile - AI Development Memory Keeper')
    parser.add_argument('command', choices=['setup', 'backup', 'record', 'history', 'handoff', 'ai-record', 'ai-stop', 'ai-history'])
    parser.add_argument('--project', '-p', default=PROJECT_NAME, help='Project name')
    parser.add_argument('--date', help='Date for history (YYYYMMDD)')
    parser.add_argument('--description', help='Change description')
    parser.add_argument('--files', nargs='+', help='Files changed')
    parser.add_argument('--chat-name', help='Chat name for handoff')
    parser.add_argument('--chat-id', help='Chat ID for handoff')
    parser.add_argument('--summary', help='Summary for handoff')
    parser.add_argument('--next-steps', help='Next steps for handoff')
    parser.add_argument('--session-name', help='AI session name')
    parser.add_argument('--session-description', help='AI session description')
    
    args = parser.parse_args()
    
    # For complex commands, delegate to the CLI
    if args.command in ['record', 'backup', 'history', 'handoff', 'ai-record', 'ai-stop', 'ai-history']:
        from src.scripts.cli import main as cli_main
        sys.argv = [sys.argv[0], args.command] + sys.argv[2:]
        cli_main()
        return
    
    # Handle simple commands directly
    if args.command == 'setup':
        setup()
    
    elif args.command == 'backup' and args.files:
        for file in args.files:
            create_backup(file, args.project)
    
    elif args.command == 'record' and args.description and args.files:
        record_change(args.description, ' '.join(args.files), args.project)
    
    elif args.command == 'history':
        show_history(args.date, args.project)
    
    elif args.command == 'handoff' and all([args.chat_name, args.chat_id, args.summary, args.next_steps]):
        generate_handoff(args.chat_name, args.chat_id, args.summary, args.next_steps, args.project)
    
    elif args.command == 'ai-record' and args.session_name and args.session_description:
        # Initialize AI tracking
        ai_tracker = AITracking(args.project)
        ai_tracker.start_session(args.session_name, args.session_description)
        log(f"Started AI session: {args.session_name}")
    
    elif args.command == 'ai-stop':
        # Stop AI tracking
        ai_tracker = AITracking(args.project)
        ai_tracker.stop_session()
        log("Stopped AI session")
    
    elif args.command == 'ai-history':
        # Show AI session history
        ai_tracker = AITracking(args.project)
        ai_tracker.show_history()

if __name__ == '__main__':
    main() 