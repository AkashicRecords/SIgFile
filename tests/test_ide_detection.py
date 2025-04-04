import os
import unittest
from unittest.mock import patch, MagicMock
from src.scripts.track_change import OptimizedCapture
from src.scripts.file_watcher import FileWatcher

class TestIDEDetection(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.capture = OptimizedCapture(enable_ai_features=False)
    
    def test_ide_detection_vscode(self):
        """Test VSCode detection."""
        with patch.dict(os.environ, {'VSCODE_PID': '1234', 'VSCODE_VERSION': '1.80.0'}):
            ide_info = self.capture._detect_ide()
            self.assertEqual(ide_info['type'], 'vscode')
            self.assertEqual(ide_info['version'], '1.80.0')
    
    def test_ide_detection_jetbrains(self):
        """Test JetBrains IDE detection."""
        with patch.dict(os.environ, {'JETBRAINS_IDE': 'PyCharm', 'JETBRAINS_IDE_VERSION': '2023.1'}):
            ide_info = self.capture._detect_ide()
            self.assertEqual(ide_info['type'], 'jetbrains')
            self.assertEqual(ide_info['version'], '2023.1')
    
    def test_ide_detection_cursor(self):
        """Test Cursor IDE detection."""
        with patch.dict(os.environ, {'CURSOR_APP': 'true', 'CURSOR_VERSION': '1.0.0'}):
            ide_info = self.capture._detect_ide()
            self.assertEqual(ide_info['type'], 'cursor')
            self.assertEqual(ide_info['version'], '1.0.0')
    
    def test_ide_detection_unknown(self):
        """Test unknown IDE detection."""
        with patch.dict(os.environ, {}, clear=True):
            ide_info = self.capture._detect_ide()
            self.assertEqual(ide_info['type'], 'unknown')
            self.assertEqual(ide_info['version'], 'unknown')

class TestFileWatcher(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.capture = OptimizedCapture(enable_ai_features=False)
    
    def test_file_watcher_initialization(self):
        """Test file watcher initialization with different IDEs."""
        # Test VSCode
        with patch.dict(os.environ, {'VSCODE_PID': '1234'}):
            capture = OptimizedCapture(enable_ai_features=False)
            self.assertIn('*.code-workspace', capture.file_watcher.ignore_patterns)
        
        # Test JetBrains
        with patch.dict(os.environ, {'JETBRAINS_IDE': 'PyCharm'}):
            capture = OptimizedCapture(enable_ai_features=False)
            self.assertIn('.idea/*', capture.file_watcher.ignore_patterns)
            self.assertIn('*.iml', capture.file_watcher.ignore_patterns)
        
        # Test Cursor
        with patch.dict(os.environ, {'CURSOR_APP': 'true'}):
            capture = OptimizedCapture(enable_ai_features=False)
            self.assertIn('cursor.config.json', capture.file_watcher.ignore_patterns)
    
    def test_handle_file_change(self):
        """Test file change handling with different IDEs."""
        # Mock the create_backup and record_change functions
        with patch('src.scripts.track_change.create_backup') as mock_backup, \
             patch('src.scripts.track_change.record_change') as mock_record:
            
            # Test with VSCode
            with patch.dict(os.environ, {'VSCODE_PID': '1234'}):
                capture = OptimizedCapture(enable_ai_features=False)
                change = {
                    'type': 'modified',
                    'path': '/test/file.py',
                    'timestamp': '2024-02-14T12:00:00'
                }
                capture._handle_file_change(change)
                
                # Verify backup was created
                mock_backup.assert_called_once_with('/test/file.py', 'logiclens')
                
                # Verify change was recorded with IDE info
                mock_record.assert_called_once()
                args = mock_record.call_args[0]
                self.assertIn('via vscode', args[0].lower())
    
    def test_ai_features_toggle(self):
        """Test AI features can be disabled."""
        capture = OptimizedCapture(enable_ai_features=False)
        self.assertFalse(capture.enable_ai_features)
        
        # Verify AI-specific code paths are not executed
        change = {
            'type': 'modified',
            'path': '/test/file.py',
            'timestamp': '2024-02-14T12:00:00'
        }
        capture._handle_file_change(change)  # Should not raise any errors about missing AI tracker

if __name__ == '__main__':
    unittest.main() 