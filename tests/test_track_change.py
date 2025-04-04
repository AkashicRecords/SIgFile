import unittest
import os
import sys
import tempfile
import shutil
import logging
import datetime
import time
import subprocess

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from scripts.track_change import (
    get_config_dirs,
    get_timestamp,
    create_backup,
    record_change,
    show_history,
    generate_handoff,
    OptimizedCapture,
    finalize_change
)

class TestTrackChange(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Configure test logging
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tracked_projects', 'sigfile', 'logs')
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Set up test logger
        self.logger = logging.getLogger('test_track_change')
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler for test logs
        test_log_file = os.path.join(self.logs_dir, 'test_track_change.log')
        file_handler = logging.FileHandler(test_log_file, mode='a')  # Append mode to keep history
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Log test start with timestamp and test name
        current_test = self.id().split('.')[-1]
        self.logger.info(f"\n{'='*80}\nStarting test: {current_test}\n{'='*80}")
        
        # Initialize test data
        self.project_name = 'sigfile'  # Use sigfile as the project name
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        with open(self.test_file, 'w') as f:
            f.write('Test content')
        
        # Initialize capture system
        self.capture = OptimizedCapture()
        self.capture.start_capture()
        
        self.logger.info(f"Test environment set up successfully for {current_test}")

    def tearDown(self):
        """Clean up test environment."""
        try:
            # First, remove immutable flags from all files in test directory
            for root, dirs, files in os.walk(self.test_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        # Remove immutable flags based on OS
                        if sys.platform == 'linux':
                            subprocess.run(['chattr', '-i', file_path], check=True)
                        elif sys.platform == 'darwin':  # macOS
                            subprocess.run(['chflags', 'nouchg', file_path], check=True)
                        elif sys.platform == 'win32':
                            subprocess.run(['attrib', '-R', '-S', '-H', file_path], check=True)
                        
                        # Make file writable
                        os.chmod(file_path, 0o666)
                    except Exception as e:
                        self.logger.warning(f"Failed to remove immutable flag from {file_path}: {str(e)}")
                
                # Make directories writable
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        os.chmod(dir_path, 0o777)
                    except Exception as e:
                        self.logger.warning(f"Failed to make directory writable {dir_path}: {str(e)}")
            
            # Now remove the test directory
            shutil.rmtree(self.test_dir, ignore_errors=True)
            
            # Clean up project directories
            project_dirs = [
                'tracked_projects/sigfile/changes',
                'tracked_projects/sigfile/backups',
                'tracked_projects/sigfile/logs',
                'tracked_projects/sigfile/docs',
                'tracked_projects/sigfile/ai_conversations',
                'tracked_projects/sigfile/thinking',
                'tracked_projects/sigfile/handoffs'
            ]
            
            for dir_path in project_dirs:
                if os.path.exists(dir_path):
                    # Remove immutable flags from all files in directory
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                if sys.platform == 'linux':
                                    subprocess.run(['chattr', '-i', file_path], check=True)
                                elif sys.platform == 'darwin':
                                    subprocess.run(['chflags', 'nouchg', file_path], check=True)
                                elif sys.platform == 'win32':
                                    subprocess.run(['attrib', '-R', '-S', '-H', file_path], check=True)
                                os.chmod(file_path, 0o666)
                            except Exception as e:
                                self.logger.warning(f"Failed to remove immutable flag from {file_path}: {str(e)}")
                    
                    # Make directory writable and remove it
                    try:
                        os.chmod(dir_path, 0o777)
                        shutil.rmtree(dir_path, ignore_errors=True)
                    except Exception as e:
                        self.logger.warning(f"Failed to remove directory {dir_path}: {str(e)}")
            
            # Clean up logs directory
            if os.path.exists('logs'):
                shutil.rmtree('logs', ignore_errors=True)
            
            # Clean up backup directory
            if os.path.exists('backup'):
                shutil.rmtree('backup', ignore_errors=True)
            
            self.logger.info("Test environment cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}", exc_info=True)
            raise

    def test_get_config_dirs(self):
        """Test configuration directory creation."""
        dirs = get_config_dirs(self.project_name)
        
        # Check if directories exist
        for dir_path in dirs.values():
            self.assertTrue(os.path.exists(dir_path))
            self.assertTrue(os.path.isdir(dir_path))
        
        self.logger.info("Configuration directories created successfully")

    def test_get_timestamp(self):
        """Test timestamp generation."""
        timestamp = get_timestamp()
        
        # Check timestamp format
        self.assertTrue(isinstance(timestamp, str))
        self.assertEqual(len(timestamp), 22)  # YYYYMMDD_HHMMSS_MMMMMM
        self.assertTrue(timestamp[8] == '_')  # Check date separator
        self.assertTrue(timestamp[15] == '_')  # Check time separator
        
        self.logger.info("Timestamp generation working correctly")

    def test_create_backup(self):
        """Test backup creation."""
        # Create a backup
        create_backup(self.test_file, self.project_name)
        
        # Get backup directory
        dirs = get_config_dirs(self.project_name)
        backup_dir = dirs['backups']
        
        # Get date directory
        date_dir = os.path.join(backup_dir, datetime.datetime.now().strftime('%Y%m%d'))
        self.assertTrue(os.path.exists(date_dir))
        
        # Check if backup was created
        backups = [f for f in os.listdir(date_dir) if os.path.isfile(os.path.join(date_dir, f))]
        self.assertTrue(len(backups) > 0)
        
        # Verify backup content
        latest_backup = max(backups)
        with open(os.path.join(date_dir, latest_backup), 'r') as f:
            content = f.read()
            self.assertEqual(content, 'Test content')

    def test_record_change(self):
        """Test change recording."""
        description = "Test change"
        files_changed = self.test_file
        
        # Record a change
        record_change(description, files_changed, self.project_name)
        
        # Get changes directory
        dirs = get_config_dirs(self.project_name)
        changes_dir = dirs['changes']
        
        # Get date directory
        date_dir = os.path.join(changes_dir, datetime.datetime.now().strftime('%Y%m%d'))
        self.assertTrue(os.path.exists(date_dir))
        
        # Check if change was recorded
        changes = [f for f in os.listdir(date_dir) if os.path.isfile(os.path.join(date_dir, f))]
        self.assertTrue(len(changes) > 0)
        
        # Verify change content
        latest_change = max(changes)
        with open(os.path.join(date_dir, latest_change), 'r') as f:
            content = f.read()
            self.assertIn(description, content)
            self.assertIn(files_changed, content)

    def test_show_history(self):
        """Test history display."""
        # Record some changes
        change_files = []
        for i in range(3):
            change_file = record_change(f"Test change {i}", self.test_file, self.project_name)
            change_files.append(change_file)
            # Finalize each change to make it immutable
            finalize_change(change_file)
            time.sleep(0.1)  # Ensure unique timestamps
        
        # Get history
        history = show_history(None, self.project_name)
        
        # Verify history content
        self.assertIsNotNone(history)
        self.assertEqual(len(history), 3)
        
        # Check that all changes are present
        for i in range(3):
            found = False
            for change in history:
                if f"Test change {i}" in change:
                    found = True
                    break
            self.assertTrue(found, f"Change {i} not found in history")
            
            # Verify the change file is immutable
            self.assertEqual(os.stat(change_files[i]).st_mode & 0o777, 0o444,
                           f"Change file {i} is not immutable")
        
        self.logger.info("History display working correctly")

    def test_generate_handoff(self):
        """Test handoff generation."""
        chat_name = "Test Chat"
        chat_id = "123"
        summary = "Test summary"
        next_steps = "Test next steps"
        
        # Generate handoff
        generate_handoff(chat_name, chat_id, summary, next_steps, self.project_name)
        
        # Get handoffs directory
        dirs = get_config_dirs(self.project_name)
        handoffs_dir = dirs['handoffs']
        
        # Get date directory
        date_dir = os.path.join(handoffs_dir, datetime.datetime.now().strftime('%Y%m%d'))
        self.assertTrue(os.path.exists(date_dir))
        
        # Check if handoff was generated
        handoffs = [f for f in os.listdir(date_dir) if os.path.isfile(os.path.join(date_dir, f))]
        self.assertTrue(len(handoffs) > 0)
        
        # Verify handoff content
        latest_handoff = max(handoffs)
        with open(os.path.join(date_dir, latest_handoff), 'r') as f:
            content = f.read()
            self.assertIn(chat_name, content)
            self.assertIn(chat_id, content)
            self.assertIn(summary, content)
            self.assertIn(next_steps, content)

    def test_capture_system(self):
        """Test capture system functionality."""
        # Verify capture system is running
        self.assertTrue(self.capture.running)
        self.logger.info("Capture system working correctly")

    def test_error_handling(self):
        """Test error handling."""
        # Test file not found
        with self.assertRaises(FileNotFoundError):
            create_backup('nonexistent.txt', self.project_name)
        
        # Test empty project name
        with self.assertRaises(ValueError):
            get_config_dirs('')
        
        # Test missing handoff fields
        with self.assertRaises(ValueError):
            generate_handoff('', '', '', '', self.project_name)
        
        self.logger.info("Error handling working correctly")

    def test_immutable_file_protection(self):
        """Test that files are properly protected with immutable flags."""
        capture = OptimizedCapture()
        test_file = os.path.join(self.test_dir, 'test_immutable.txt')
        
        # Create a test file
        with open(test_file, 'w') as f:
            f.write('test content')
        
        # Make it immutable
        capture._make_immutable(test_file)
        
        # Verify read-only permissions
        stat_info = os.stat(test_file)
        self.assertEqual(stat_info.st_mode & 0o777, 0o444)
        
        # Verify immutable flag based on OS
        if sys.platform == 'linux':
            result = subprocess.run(['lsattr', test_file], capture_output=True, text=True)
            self.assertIn('i', result.stdout)
        elif sys.platform == 'darwin':  # macOS
            result = subprocess.run(['ls', '-lO', test_file], capture_output=True, text=True)
            self.assertIn('uchg', result.stdout)
        elif sys.platform == 'win32':
            result = subprocess.run(['attrib', test_file], capture_output=True, text=True)
            self.assertIn('R', result.stdout)
            self.assertIn('S', result.stdout)
            self.assertIn('H', result.stdout)
        
        # Verify file cannot be modified
        with self.assertRaises(PermissionError):
            with open(test_file, 'w') as f:
                f.write('new content')
        
        # Verify file cannot be deleted
        with self.assertRaises(PermissionError):
            os.remove(test_file)

    def test_directory_setup_with_protection(self):
        """Test that directory setup creates and protects all required files."""
        capture = OptimizedCapture()
        capture._setup_directories()
        
        # Check all required directories exist
        required_dirs = ['changes', 'backups', 'logs', 'docs', 
                        'ai_conversations', 'thinking', 'handoffs']
        for dir_name in required_dirs:
            dir_path = os.path.join('tracked_projects', 'sigfile', dir_name)
            self.assertTrue(os.path.exists(dir_path))
            
            # Check .gitkeep exists and is protected
            gitkeep_path = os.path.join(dir_path, '.gitkeep')
            self.assertTrue(os.path.exists(gitkeep_path))
            self.assertEqual(os.stat(gitkeep_path).st_mode & 0o777, 0o444)
            
            # Check README.txt exists and is protected
            readme_path = os.path.join(dir_path, 'README.txt')
            self.assertTrue(os.path.exists(readme_path))
            self.assertEqual(os.stat(readme_path).st_mode & 0o777, 0o444)
        
        # Check main documentation files
        docs_dir = os.path.join('tracked_projects', 'sigfile', 'docs')
        required_files = ['file_structure.txt', 'README.txt']
        for filename in required_files:
            file_path = os.path.join(docs_dir, filename)
            self.assertTrue(os.path.exists(file_path))
            self.assertEqual(os.stat(file_path).st_mode & 0o777, 0o444)
        
        # Check change history exists and is protected
        history_path = os.path.join('tracked_projects', 'sigfile', 'changes', 'change_history.txt')
        self.assertTrue(os.path.exists(history_path))
        self.assertEqual(os.stat(history_path).st_mode & 0o777, 0o444)

    def test_change_history_preservation(self):
        """Test that existing change history is preserved during setup."""
        capture = OptimizedCapture()
        
        # Create initial change history
        history_dir = os.path.join('tracked_projects', 'sigfile', 'changes')
        os.makedirs(history_dir, exist_ok=True)
        history_path = os.path.join(history_dir, 'change_history.txt')
        
        initial_content = "# Initial History\nTest content"
        with open(history_path, 'w') as f:
            f.write(initial_content)
        
        # Run setup
        capture._setup_directories()
        
        # Verify history was preserved and new content was added
        with open(history_path, 'r') as f:
            content = f.read()
            self.assertIn(initial_content, content)
            self.assertIn("System Setup", content)

    def test_directory_permission_verification(self):
        """Test directory permission verification."""
        capture = OptimizedCapture()
        test_dir = os.path.join(self.test_dir, 'perm_test')
        os.makedirs(test_dir)
        
        # Test with writable directory
        capture._verify_directory_permissions(test_dir)
        
        # Test with read-only directory
        os.chmod(test_dir, 0o444)
        with self.assertRaises(Exception):
            capture._verify_directory_permissions(test_dir)

if __name__ == '__main__':
    unittest.main() 