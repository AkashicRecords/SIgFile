#!/usr/bin/env python3

import os
import stat
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('setup_immutable_files')

def make_immutable(file_path):
    """Make a file immutable using both chmod and chattr."""
    try:
        # First set read-only permissions (0o444)
        os.chmod(file_path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
        
        # Then make it immutable using chattr
        subprocess.run(['chattr', '+i', file_path], check=True)
        
        logger.info(f"Made file immutable: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error making file immutable: {str(e)}")
        return False

def setup_project_files():
    """Set up project files with immutable permissions."""
    base_dir = os.path.join('tracked_projects', 'sigfile')
    
    # Define the directory structure and files
    structure = {
        'changes': {
            '20240403': {
                'change_history.txt': '# Change History - April 3, 2024\n\n## File Structure Changes\n1. Created tracked_projects/sigfile/docs/file_structure.txt\n   - Added comprehensive documentation of project structure\n   - Documented file purposes and contents\n   - Added change tracking format specifications',
                'changes_20240403_060000.txt': '# Changes Record - April 3, 2024\n\n## Changes Made\n1. Fixed directory structure issues\n2. Implemented immutable file permissions\n3. Enhanced error handling',
            }
        },
        'docs': {
            'file_structure.txt': '# SigFile Project Structure Documentation\n\n## Root Directory Structure\n/\n├── src/                    # Source code directory\n│   └── scripts/           # Python scripts\n│       ├── track_change.py # Main change tracking functionality\n│       └── file_watcher.py # File watching and change detection\n├── tests/                 # Test files\n│   └── test_track_change.py # Unit tests for change tracking\n├── tracked_projects/      # Project-specific tracked data\n│   └── sigfile/          # SigFile project data\n│       ├── changes/      # Recorded file changes\n│       ├── backups/      # File backups\n│       ├── logs/         # Application logs\n│       └── docs/         # Project documentation',
            'README.txt': '# SigFile Project Documentation\n\nThis directory contains immutable project documentation and change history.\nThese files cannot be modified or deleted to ensure project history preservation.'
        }
    }
    
    # Create directories and files
    for dir_name, contents in structure.items():
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        
        if isinstance(contents, dict):
            for subdir, files in contents.items():
                subdir_path = os.path.join(dir_path, subdir)
                os.makedirs(subdir_path, exist_ok=True)
                
                if isinstance(files, dict):
                    for filename, content in files.items():
                        file_path = os.path.join(subdir_path, filename)
                        with open(file_path, 'w') as f:
                            f.write(content)
                        make_immutable(file_path)
                else:
                    # Handle direct files in docs directory
                    file_path = os.path.join(dir_path, subdir)
                    with open(file_path, 'w') as f:
                        f.write(files)
                    make_immutable(file_path)
    
    logger.info("Project files set up successfully with immutable permissions")

if __name__ == '__main__':
    setup_project_files() 