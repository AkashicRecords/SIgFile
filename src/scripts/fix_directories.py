#!/usr/bin/env python3

import os
import sys
from track_change import get_config_dirs, logger

def fix_directory_structure():
    """Fix the directory structure for the sigfile project."""
    try:
        # Get the directories for the sigfile project
        dirs = get_config_dirs('sigfile')
        
        # Create .gitkeep files in empty directories
        for dir_path in dirs.values():
            gitkeep_file = os.path.join(dir_path, '.gitkeep')
            if not os.path.exists(gitkeep_file):
                with open(gitkeep_file, 'w') as f:
                    f.write('')
                logger.info(f"Created .gitkeep in {dir_path}")
                
        logger.info("Directory structure fixed successfully")
        
    except Exception as e:
        logger.error(f"Error fixing directory structure: {str(e)}")
        raise

if __name__ == '__main__':
    fix_directory_structure() 