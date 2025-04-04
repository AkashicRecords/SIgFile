from setuptools import setup, find_packages
import os
import sys

# Determine if this is a development or release build
is_dev_build = os.environ.get('SIGFILE_DEV_BUILD', '0') == '1'

# Common dependencies
install_requires = [
    "typer>=0.4.0",
    "rich>=10.12.0",
    "python-dotenv>=0.19.0",
    "pyyaml>=5.4.1",
    "click>=8.0.3",
    "prompt_toolkit>=3.0.20",
    "pygments>=2.10.0",
    "python-dateutil>=2.8.2",
    "pytz>=2021.1",
]

# Development-specific dependencies
dev_requires = [
    "pytest>=7.4.4",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.10.0",
    "coverage>=7.2.7",
    "black>=22.3.0",
    "isort>=5.10.1",
    "flake8>=4.0.1",
    "mypy>=0.950",
    "pre-commit>=2.20.0",
    "bandit>=1.7.0",  # Security scanning
    "safety>=2.3.5",  # Dependency security checking
]

# Release-specific dependencies
release_requires = [
    "pyinstaller>=5.0.0",  # For creating standalone executables
    "cython>=0.29.24",     # For performance optimization
]

# Package data
package_data = {
    'sigfile_cli': [
        'templates/*',
        'config/*',
    ]
}

# Entry points
entry_points = {
    "console_scripts": [
        "sigfile=sigfile_cli.cli:app",
    ],
}

# Development-specific configurations
if is_dev_build:
    print("Building development version...")
    # Add development-specific package data
    package_data['sigfile_cli'].extend([
        'tests/*',
        'docs/*',
    ])
    # Add development-specific entry points
    entry_points["console_scripts"].extend([
        "sigfile-dev=sigfile_cli.cli:dev_app",
    ])

setup(
    name="sigfile-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        "release": release_requires,
    },
    package_data=package_data,
    python_requires=">=3.7",
    author="Sam Elder",
    author_email="samelder@example.com",
    description="Command-line interface for the SigFile development process tracking tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AkashicRecords/SigFile-CLI",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points=entry_points,
    # Release-specific configurations
    options={
        'build': {
            'optimize': 2 if not is_dev_build else 0,  # Optimize bytecode for release
        },
        'bdist_wheel': {
            'universal': True,
        },
    },
    # Security and IP protection
    zip_safe=False,  # Prevent direct access to source files
    include_package_data=True,
) 