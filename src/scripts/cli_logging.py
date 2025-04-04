#!/usr/bin/env python3

import os
import sys
import logging
from pathlib import Path
from typing import Optional

class CLILogger:
    """Logger configuration for CLI tool."""
    
    def __init__(self, project_name: str = "sigfile"):
        self.project_name = project_name
        self.logger = logging.getLogger('sigfile_cli')
        self.setup_logging()
    
    def setup_logging(self):
        """Set up logging configuration for CLI tool."""
        # Create logs directory if it doesn't exist
        logs_dir = Path(__file__).parent.parent / 'logs' / self.project_name
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Clear any existing handlers
        self.logger.handlers = []
        
        # Set log level based on environment
        self.logger.setLevel(logging.DEBUG if os.getenv('SIGFILE_DEBUG') else logging.INFO)
        
        # Console handler with color formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for detailed logs
        log_file = logs_dir / 'cli.log'
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Add command execution logging
        self.logger.info(f"CLI tool initialized for project: {self.project_name}")
    
    def log_command(self, command: str, args: Optional[dict] = None):
        """Log command execution."""
        self.logger.debug(f"Executing command: {command}")
        if args:
            self.logger.debug(f"Command arguments: {args}")
    
    def log_error(self, error: Exception, context: Optional[str] = None):
        """Log error with context."""
        self.logger.error(f"Error occurred: {str(error)}")
        if context:
            self.logger.error(f"Context: {context}")
        self.logger.error("Stack trace:", exc_info=True)
    
    def log_success(self, message: str):
        """Log successful operation."""
        self.logger.info(f"Success: {message}")
    
    def log_warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def log_debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)

# Create global logger instance
cli_logger = CLILogger() 