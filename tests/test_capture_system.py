import unittest
from unittest.mock import Mock, patch
import tempfile
import shutil
from pathlib import Path
import os
import stat
from datetime import datetime
import time
from src.scripts.track_change import OptimizedCapture

class TestOptimizedCapture(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Initialize capture system
        self.capture = OptimizedCapture()

    def tearDown(self):
        """Clean up after each test"""
        # Stop capture if running
        if hasattr(self, 'capture'):
            self.capture.stop_capture()
        
        # Restore original directory
        os.chdir(self.original_cwd)
        
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

    def test_directory_creation(self):
        """Test directory creation and permissions"""
        # Check base directories
        expected_dirs = [
            'logs',
            'tracked_projects',
            'tracked_projects/backups',
            'tracked_projects/changes',
            'tracked_projects/ai_conversations',
            'tracked_projects/thinking',
            'tracked_projects/handoffs'
        ]
        
        for dir_path in expected_dirs:
            path = Path(dir_path)
            self.assertTrue(path.exists(), f"Directory {dir_path} should exist")
            self.assertTrue(path.is_dir(), f"{dir_path} should be a directory")
            
            # Check permissions (755)
            mode = path.stat().st_mode
            self.assertEqual(
                mode & 0o777,
                0o755,
                f"Directory {dir_path} should have 755 permissions"
            )

    def test_project_directories(self):
        """Test project-specific directory creation"""
        projects = ['sigfile', 'logiclens']
        subdirs = ['changes', 'backups', 'ai_conversations', 'thinking', 'handoffs']
        
        for project in projects:
            for subdir in subdirs:
                path = Path(f'tracked_projects/{project}/{subdir}')
                self.assertTrue(path.exists(), f"Project directory {path} should exist")
                self.assertTrue(path.is_dir(), f"{path} should be a directory")
                
                # Check .gitkeep file
                gitkeep = path / '.gitkeep'
                self.assertTrue(gitkeep.exists(), f".gitkeep should exist in {path}")
                self.assertEqual(
                    gitkeep.stat().st_mode & 0o777,
                    0o600,
                    f".gitkeep in {path} should have 600 permissions"
                )

    def test_logging_setup(self):
        """Test logging configuration"""
        # Check log files exist
        today = datetime.now().strftime('%Y%m%d')
        log_files = [
            f'logs/capture_{today}.log',
            f'logs/errors_{today}.log'
        ]
        
        for log_file in log_files:
            path = Path(log_file)
            self.assertTrue(path.exists(), f"Log file {log_file} should exist")
            self.assertTrue(path.is_file(), f"{log_file} should be a file")
            
            # Check permissions (644)
            self.assertEqual(
                path.stat().st_mode & 0o777,
                0o644,
                f"Log file {log_file} should have 644 permissions"
            )

    @patch('threading.Thread')
    def test_capture_start(self, mock_thread):
        """Test capture system startup"""
        # Mock thread creation
        mock_thread.return_value = Mock()
        
        # Start capture
        self.capture.start_capture()
        
        # Verify threads were created
        self.assertEqual(mock_thread.call_count, 3, "Should create 3 capture threads")

    def test_queue_limits(self):
        """Test queue size limits"""
        self.assertEqual(self.capture.chat_queue.maxsize, 1000)
        self.assertEqual(self.capture.file_queue.maxsize, 1000)
        self.assertEqual(self.capture.thinking_queue.maxsize, 1000)

    @patch('logging.Logger')
    def test_error_logging(self, mock_logger):
        """Test error logging functionality"""
        # Simulate an error
        test_error = Exception("Test error")
        self.capture.logger.error("Test error", exc_info=True)
        
        # Verify error was logged
        mock_logger.error.assert_called_with("Test error", exc_info=True)

    def test_stop_capture(self):
        """Test capture system shutdown"""
        # Start capture
        self.capture.start_capture()
        
        # Stop capture
        self.capture.stop_capture()
        
        # Verify stop event is set
        self.assertTrue(self.capture.stop_event.is_set())

class TestCaptureThreads(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.capture = OptimizedCapture()

    def tearDown(self):
        if hasattr(self, 'capture'):
            self.capture.stop_capture()
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    @patch('time.sleep')
    def test_chat_capture(self, mock_sleep):
        """Test chat capture functionality"""
        # Mock chat proxy
        self.capture.chat_proxy = Mock()
        self.capture.chat_proxy.capture.return_value = {"message": "test"}
        
        # Start capture
        self.capture.start_capture()
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Stop capture
        self.capture.stop_capture()
        
        # Verify chat proxy was called
        self.capture.chat_proxy.capture.assert_called()

    @patch('time.sleep')
    def test_file_capture(self, mock_sleep):
        """Test file capture functionality"""
        # Mock file watcher
        self.capture.file_watcher = Mock()
        self.capture.file_watcher.watch.return_value = {"file": "test.txt"}
        
        # Start capture
        self.capture.start_capture()
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Stop capture
        self.capture.stop_capture()
        
        # Verify file watcher was called
        self.capture.file_watcher.watch.assert_called()

    @patch('time.sleep')
    def test_thinking_capture(self, mock_sleep):
        """Test thinking capture functionality"""
        # Mock thinking capture
        self.capture.thinking_capture = Mock()
        self.capture.thinking_capture.record.return_value = {"thought": "test"}
        
        # Start capture
        self.capture.start_capture()
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Stop capture
        self.capture.stop_capture()
        
        # Verify thinking capture was called
        self.capture.thinking_capture.record.assert_called()

if __name__ == '__main__':
    unittest.main() 