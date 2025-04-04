import os
from typing import Dict, Any

# Determine build type
IS_DEV_BUILD = os.environ.get('SIGFILE_DEV_BUILD', '0') == '1'

# Common configuration
COMMON_CONFIG: Dict[str, Any] = {
    'version': '0.1.0',
    'author': 'Sam Elder',
    'email': 'samelder@example.com',
    'description': 'Command-line interface for the SigFile development process tracking tool',
    'url': 'https://github.com/AkashicRecords/SigFile-CLI',
}

# Development configuration
DEV_CONFIG: Dict[str, Any] = {
    'debug': True,
    'log_level': 'DEBUG',
    'enable_profiling': True,
    'enable_coverage': True,
    'enable_type_checking': True,
    'enable_linting': True,
    'enable_security_checks': True,
    'enable_performance_monitoring': True,
    'include_tests': True,
    'include_docs': True,
    'optimize_level': 0,  # No optimization for development
}

# Release configuration
RELEASE_CONFIG: Dict[str, Any] = {
    'debug': False,
    'log_level': 'INFO',
    'enable_profiling': False,
    'enable_coverage': False,
    'enable_type_checking': False,
    'enable_linting': False,
    'enable_security_checks': True,
    'enable_performance_monitoring': False,
    'include_tests': False,
    'include_docs': False,
    'optimize_level': 2,  # Maximum optimization for release
    'strip_docstrings': True,
    'strip_assertions': True,
    'strip_comments': True,
    'enable_bytecode_optimization': True,
    'enable_cython_compilation': True,
}

# Get current configuration
def get_config() -> Dict[str, Any]:
    """Get the current build configuration."""
    config = COMMON_CONFIG.copy()
    if IS_DEV_BUILD:
        config.update(DEV_CONFIG)
    else:
        config.update(RELEASE_CONFIG)
    return config

# Build configuration
BUILD_CONFIG = get_config() 