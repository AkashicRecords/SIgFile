# SigFile.ai - Your Digital Memory Keeper

> "In the digital age, your development history is your most valuable asset. SigFile.ai helps you preserve it."

## What is SigFile?

SigFile.ai is a universal change tracking and backup system that works with any application or development environment. While it was initially designed for development environments, it can be used to track changes in:

- Any development environment (VS Code, IntelliJ, Sublime Text, etc.)
- Configuration files
- System settings
- Project documentation
- Any other files or directories you want to track

Key benefits:
- Works independently of any specific IDE or application
- Can track changes across multiple projects simultaneously
- Maintains a clear history of modifications
- Provides easy rollback capabilities
- Generates comprehensive handoff documentation

### Platform Compatibility
- **macOS**: Fully supported (see macOS Setup)
- **Windows**: Fully supported (see Windows Setup)
- **Linux**: Not currently supported

### Use Cases

1. **Development Environments**
   - Track IDE settings and configurations
   - Monitor development environment changes
   - Document tool-specific customizations

2. **Project Management**
   - Track project configuration changes
   - Monitor dependency updates
   - Document architectural decisions

3. **System Administration**
   - Track system configuration changes
   - Monitor environment setup modifications
   - Document infrastructure changes

4. **Documentation**
   - Track documentation updates
   - Monitor README changes
   - Document API modifications

## Getting Started

### Prerequisites
1. Ensure you have the required dependencies:
   ```bash
   # On macOS
   brew install moreutils
   
   # On Ubuntu/Debian
   sudo apt-get install moreutils
   ```

2. Clone the SigFile repository to your home directory:
   ```bash
   # Create and navigate to SigFile directory
   mkdir -p ~/sigfile
   cd ~/sigfile
   
   # Clone the repository
   git clone https://github.com/AkashicRecords/SigFile.git .
   ```

3. Make the tracking script executable:
   ```bash
   chmod +x src/scripts/track_change.sh
   ```

4. Create a symbolic link for global access:
   ```bash
   # This makes SigFile accessible from anywhere
   ln -s ~/sigfile/src/scripts/track_change.sh /usr/local/bin/sigfile
   ```

### Using SigFile with Any Application

1. **Access from Any Directory**
   - Once set up, you can use SigFile from any directory by typing `sigfile`:
   ```bash
   # Basic command structure
   sigfile [command] [options]
   ```

2. **Setting Up for a New Application**
   ```bash
   # Navigate to your application directory
   cd /path/to/your/app
   
   # Initialize SigFile for this application
   sigfile setup
   
   # Start tracking changes (replace "myapp" with your app name)
   sigfile -p myapp record "Initial setup" "config/*"
   ```

3. **Directory Structure**
   - SigFile creates a `tracked_projects` directory in your home folder:
   ```
   ~/tracked_projects/
   └── myapp/                    # Your application name
       ├── changes/             # Change logs
       │   └── YYYYMMDD/       # Organized by date
       ├── backups/            # File backups
       │   └── YYYYMMDD/      # Organized by date
       └── handoffs/          # Handoff documents
           └── YYYYMMDD/     # Organized by date
   ```

4. **Quick Start Examples**
   ```bash
   # From any directory, track changes for your app
   sigfile -p myapp record "Updated settings" "config.json"
   
   # Create a backup
   sigfile -p myapp backup config.json
   
   # Generate a handoff document
   sigfile -p myapp handoff "Feature Update" "chat_123" "Added new feature" "Test changes"
   
   # View change history
   sigfile -p myapp history
   ```

### Best Practices

1. **Regular Backups**
   - Create backups before making significant changes
   - Backup configuration files regularly
   - Use meaningful backup descriptions

2. **Change Tracking**
   - Record changes as they happen
   - Include clear descriptions
   - List all affected files

3. **Handoff Documents**
   - Generate handoffs after major changes
   - Include clear next steps
   - Document important decisions

4. **Project Organization**
   - Use consistent project names
   - Keep related changes together
   - Regular cleanup of old backups

## Core Features

### 1. Intelligent Change Tracking
- Automatically records changes with timestamps
- Organizes changes by date and project
- Maintains a clear history of modifications
- Supports multiple project tracking

### 2. Smart Backup System
- Creates automatic backups before changes
- Organizes backups by date
- Easy restoration of previous states
- Version control for configuration files

### 3. Handoff Documentation
- Generates comprehensive handoff documents
- Tracks chat history and decisions
- Maintains project context
- Supports team collaboration

### 4. Project-Specific Tracking
- Separate tracking for different projects
- Organized directory structure
- Clear separation of concerns
- Easy project management

## Command Usage Guide

### Basic Commands

```bash
# Initialize SigFile
./src/scripts/track_change.sh setup

# Record a change
./src/scripts/track_change.sh record "description" "files_changed"

# Create a backup
./src/scripts/track_change.sh backup <file>

# Show change history
./src/scripts/track_change.sh history [YYYYMMDD]

# Generate handoff document
./src/scripts/track_change.sh handoff "chat_name" "chat_id" "summary" "next_steps"
```

### Project-Specific Commands

```bash
# Record a change for a specific project
./src/scripts/track_change.sh -p project_name record "description" "files_changed"

# Create a backup for a specific project
./src/scripts/track_change.sh -p project_name backup <file>

# Show history for a specific project
./src/scripts/track_change.sh -p project_name history [YYYYMMDD]

# Generate handoff for a specific project
./src/scripts/track_change.sh -p project_name handoff "chat_name" "chat_id" "summary" "next_steps"
```

### Command Details

#### Record Changes
```bash
./src/scripts/track_change.sh record "description" "files_changed"
```
- Records a change with timestamp
- Creates a markdown file in `tracked_projects/<project>/changes/YYYYMMDD/`
- Includes description and files changed

#### Create Backups
```bash
./src/scripts/track_change.sh backup <file>
```
- Creates a timestamped backup of the specified file
- Stores in `tracked_projects/<project>/backups/YYYYMMDD/`
- Preserves original file permissions

#### View History
```bash
./src/scripts/track_change.sh history [YYYYMMDD]
```
- Shows all changes for the specified date
- If no date provided, shows today's changes
- Displays in chronological order

#### Generate Handoff
```bash
./src/scripts/track_change.sh handoff "chat_name" "chat_id" "summary" "next_steps"
```
- Creates a comprehensive handoff document
- Includes chat information, summary, and next steps
- Stores in `tracked_projects/<project>/handoffs/YYYYMMDD/`

### Examples

```bash
# Record a change to multiple files
./src/scripts/track_change.sh record "Updated API endpoints" "api.py, routes.py, config.py"

# Create a backup of a configuration file
./src/scripts/track_change.sh backup config/settings.json

# View all changes from a specific date
./src/scripts/track_change.sh history 20250326

# Generate a handoff document
./src/scripts/track_change.sh handoff "API Integration" "chat_123" "Completed API endpoints" "Test new endpoints"

# Track changes for a specific project
./src/scripts/track_change.sh -p frontend record "Updated UI components" "components/*"
```

## Project Structure

```
sigfile/
├── src/
│   └── scripts/
│       └── track_change.sh    # Main tracking script
├── tracked_projects/          # Projects being tracked
│   └── logiclens/            # LogicLens project tracking
│       ├── changes/          # Change logs
│       │   └── YYYYMMDD/     # Organized by date
│       ├── backups/          # File backups
│       │   └── YYYYMMDD/     # Organized by date
│       └── handoffs/         # Handoff documents
│           └── YYYYMMDD/     # Organized by date
└── [configuration files]
```

## Future Vision

### Planned Features
- AI-powered change analysis
- Automated rollback suggestions
- Integration with popular IDEs
- Cloud backup support
- Team collaboration features

### Use Cases
- Development environment management
- Configuration tracking
- Team handoffs
- Project history preservation
- Disaster recovery

## Dependencies

### macOS Dependencies
```bash
# Core dependencies
brew install moreutils    # For timestamp functionality
brew install coreutils    # For enhanced GNU utilities
brew install tree        # For directory visualization
brew install jq          # For JSON processing

# Optional but recommended
brew install git        # For version control integration
brew install ripgrep    # For fast file searching
```

### Windows Dependencies
1. **PowerShell 5.0 or later**
   ```powershell
   $PSVersionTable.PSVersion
   ```

2. **Git for Windows**
   - Download from: https://git-scm.com/download/win
   - Required for version control integration

3. **Visual Studio Integration**
   - Visual Studio 2019 or later
   - Visual Studio Code
   - Windows Terminal (recommended)

4. **Optional Dependencies**
   - Windows Subsystem for Linux (WSL) - for enhanced functionality
   - Git Bash - for Unix-like commands

### Shell Requirements
- **macOS**: zsh shell (default on modern macOS)
- **Windows**: PowerShell 5.0 or later

### File System Requirements
- Case-sensitive file system (recommended)
- At least 1GB free space for backups
- Write permissions in user directory

### Network Requirements
- Internet connection for initial setup
- Optional: Git for version control integration

## Setup Instructions

### macOS Setup
```bash
# Clone the repository
mkdir -p ~/sigfile
cd ~/sigfile
git clone https://github.com/AkashicRecords/SigFile.git .

# Make the script executable
chmod +x src/scripts/track_change.sh

# Create symbolic link
ln -s ~/sigfile/src/scripts/track_change.sh /usr/local/bin/sigfile
```

### Windows Setup
1. **Install Dependencies**
   ```powershell
   # Install Chocolatey if not installed
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

   # Install Git
   choco install git -y
   ```

2. **Clone the Repository**
   ```powershell
   # Create and navigate to SigFile directory
   mkdir $env:USERPROFILE\sigfile
   cd $env:USERPROFILE\sigfile
   
   # Clone the repository
   git clone https://github.com/AkashicRecords/SigFile.git .
   ```

3. **Set Up PowerShell Profile**
   ```powershell
   # Open PowerShell profile
   notepad $PROFILE
   
   # Add SigFile alias
   Set-Alias -Name sigfile -Value "$env:USERPROFILE\sigfile\src\scripts\track_change.ps1"
   ```

4. **Visual Studio Integration**
   - **Visual Studio**
     ```powershell
     # Track VS settings
     sigfile -p visualstudio record "Updated VS settings" "$env:APPDATA\Microsoft\VisualStudio\*"
     
     # Backup solution file
     sigfile -p visualstudio backup "MySolution.sln"
     ```
   
   - **Visual Studio Code**
     ```powershell
     # Track VS Code settings
     sigfile -p vscode record "Updated VS Code settings" "$env:APPDATA\Code\User\settings.json"
     
     # Backup workspace settings
     sigfile -p vscode backup ".vscode/settings.json"
     ```

### Installation Verification
```powershell
# Check PowerShell version
$PSVersionTable.PSVersion

# Check dependencies
Get-Command git -ErrorAction SilentlyContinue
Get-Command tree -ErrorAction SilentlyContinue
```

### Troubleshooting Dependencies
If you encounter issues:

1. **PowerShell Version**
   ```powershell
   # Update PowerShell
   winget install Microsoft.PowerShell
   ```

2. **Git not found**
   ```powershell
   # Install Git
   choco install git -y
   ```

3. **Permission issues**
   ```powershell
   # Fix execution policy
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Path issues**
   ```powershell
   # Add SigFile to PATH
   $env:Path += ";$env:USERPROFILE\sigfile\src\scripts"
   ```

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- Inspired by the need for better development environment management
- Built with modern shell scripting best practices
- Designed for developer productivity 

## Using SigFile with Different Applications

### Visual Studio
```powershell
# Track VS settings
sigfile -p visualstudio record "Updated VS settings" "$env:APPDATA\Microsoft\VisualStudio\*"

# Backup solution file
sigfile -p visualstudio backup "MySolution.sln"

# Track project changes
sigfile -p visualstudio record "Added new feature" "ProjectName/*.cs"
```

### Visual Studio Code
```powershell
# Track VS Code settings
sigfile -p vscode record "Updated VS Code settings" "$env:APPDATA\Code\User\settings.json"

# Backup workspace settings
sigfile -p vscode backup ".vscode/settings.json"

# Track extension changes
sigfile -p vscode record "Installed new extensions" "$env:USERPROFILE\.vscode\extensions"
```

### IntelliJ/WebStorm
```powershell
# Track IDE settings
sigfile -p intellij record "Updated IDE settings" "$env:APPDATA\JetBrains\*"

# Backup project settings
sigfile -p intellij backup ".idea/*"
```

### Sublime Text
```powershell
# Track Sublime settings
sigfile -p sublime record "Updated Sublime settings" "$env:APPDATA\Sublime Text\Packages\User"

# Backup user preferences
sigfile -p sublime backup "Preferences.sublime-settings"
```

### Git Projects
```powershell
# Track git configuration
sigfile -p git record "Updated git config" "$env:USERPROFILE\.gitconfig"

# Backup git hooks
sigfile -p git backup ".git/hooks/*"
```

### Docker Projects
```powershell
# Track Docker configuration
sigfile -p docker record "Updated Docker settings" "docker-compose.yml"

# Backup Docker files
sigfile -p docker backup "Dockerfile"
```

## Complete Command Reference

### Basic Commands

#### Setup
```powershell
# Initialize SigFile
sigfile setup

# Initialize for specific project
sigfile -p projectname setup
```

#### Record Changes
```powershell
# Basic change recording
sigfile record "description" "files_changed"

# Project-specific change
sigfile -p projectname record "description" "files_changed"

# Record with multiple files
sigfile record "Updated multiple files" "file1.txt, file2.txt, dir/*"
```

#### Create Backups
```powershell
# Basic backup
sigfile backup <file>

# Project-specific backup
sigfile -p projectname backup <file>

# Backup multiple files
sigfile backup "file1.txt, file2.txt"
```

#### View History
```powershell
# View today's changes
sigfile history

# View specific date
sigfile history -Date 20250326

# View project history
sigfile -p projectname history

# View project history for date
sigfile -p projectname history -Date 20250326
```

#### Generate Handoff
```powershell
# Basic handoff
sigfile handoff "chat_name" "chat_id" "summary" "next_steps"

# Project-specific handoff
sigfile -p projectname handoff "chat_name" "chat_id" "summary" "next_steps"
```

### Command Options

#### Global Options
- `-p, --project <name>`: Specify project name
- `-v, --verbose`: Enable verbose output
- `-d, --debug`: Enable debug mode

#### Record Options
- `--description <text>`: Change description
- `--files <pattern>`: Files changed
- `--tags <tags>`: Add tags to change

#### Backup Options
- `--file <path>`: File to backup
- `--force`: Force backup overwrite
- `--compress`: Compress backup

#### History Options
- `--date <YYYYMMDD>`: View specific date
- `--project <name>`: View project history
- `--format <format>`: Output format (text/json)

#### Handoff Options
- `--chat-name <name>`: Chat name
- `--chat-id <id>`: Chat ID
- `--summary <text>`: Change summary
- `--next-steps <text>`: Next steps

### Examples

#### Development Environment
```powershell
# Track VS Code settings
sigfile -p vscode record "Updated settings" "$env:APPDATA\Code\User\settings.json"

# Backup VS Code extensions
sigfile -p vscode backup "$env:USERPROFILE\.vscode\extensions"
```

#### Project Management
```powershell
# Track project changes
sigfile -p myproject record "Added new feature" "src/features/*"

# Backup project config
sigfile -p myproject backup "config.json"
```

#### System Configuration
```powershell
# Track system settings
sigfile -p system record "Updated environment" "$env:USERPROFILE\.profile"

# Backup system config
sigfile -p system backup "system.json"
``` 