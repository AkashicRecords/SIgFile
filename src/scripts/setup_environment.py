#!/usr/bin/env python3

import os
import sys
import subprocess
import platform
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_virtual_environment():
    """Create a virtual environment named 'Sigfile'."""
    try:
        # Check if Sigfile venv already exists
        if os.path.exists('Sigfile'):
            logger.info("Virtual environment 'Sigfile' already exists")
            return True

        # Create virtual environment
        logger.info("Creating virtual environment 'Sigfile'...")
        subprocess.run([sys.executable, '-m', 'venv', 'Sigfile'], check=True)
        
        # Determine activation script based on platform
        if platform.system() == 'Windows':
            activate_script = os.path.join('Sigfile', 'Scripts', 'activate')
        else:
            activate_script = os.path.join('Sigfile', 'bin', 'activate')
        
        # Make activation script executable on Unix-like systems
        if platform.system() != 'Windows':
            os.chmod(activate_script, 0o755)
        
        logger.info("Virtual environment 'Sigfile' created successfully")
        logger.info(f"To activate the virtual environment, run:")
        if platform.system() == 'Windows':
            logger.info("    .\\Sigfile\\Scripts\\activate")
        else:
            logger.info("    source Sigfile/bin/activate")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating virtual environment: {str(e)}")
        return False

def install_dependencies():
    """Install required dependencies."""
    try:
        # Determine pip executable based on platform
        if platform.system() == 'Windows':
            pip_executable = os.path.join('Sigfile', 'Scripts', 'pip')
        else:
            pip_executable = os.path.join('Sigfile', 'bin', 'pip')
        
        # Install dependencies
        logger.info("Installing dependencies...")
        subprocess.run([pip_executable, 'install', '-r', 'requirements.txt'], check=True)
        logger.info("Dependencies installed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error installing dependencies: {str(e)}")
        return False

def main():
    """Main setup function."""
    logger.info("Starting SigFile setup...")
    
    # Create virtual environment
    if not create_virtual_environment():
        logger.error("Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        logger.error("Failed to install dependencies")
        sys.exit(1)
    
    logger.info("SigFile setup completed successfully!")

if __name__ == "__main__":
    main() 