# Development Mode

Development mode is a feature in SigFile that allows you to temporarily bypass permission restrictions during development. This is useful when you need to make changes to files that would normally be protected by the role-based permission system.

## Overview

Development mode provides a way to temporarily disable the permission system for specific files or all files in your project. This allows you to make changes without having to constantly grant and revoke permissions for different roles.

## Usage

### Command Line Interface

The easiest way to manage development mode is through the command line interface:

```bash
# Enable development mode for all files
python -m src.scripts.cli dev-mode enable

# Enable development mode for a specific file
python -m src.scripts.cli dev-mode enable --file path/to/file

# Disable development mode for all files
python -m src.scripts.cli dev-mode disable

# Disable development mode for a specific file
python -m src.scripts.cli dev-mode disable --file path/to/file
```

### Python API

You can also manage development mode programmatically:

```python
from src.scripts.permission_manager import permission_manager

# Enable development mode for all files
permission_manager.enable_dev_mode()

# Enable development mode for a specific file
permission_manager.enable_dev_mode("path/to/file")

# Disable development mode for all files
permission_manager.disable_dev_mode()

# Disable development mode for a specific file
permission_manager.disable_dev_mode("path/to/file")
```

## How It Works

When development mode is enabled:

1. The permission system checks if development mode is enabled for the file being accessed
2. If development mode is enabled, all permission checks are bypassed
3. The file's immutable flags are temporarily removed
4. When development mode is disabled, the immutable flags are restored

## Security Considerations

Development mode should be used carefully and disabled when not needed to maintain system security:

1. **Temporary Use**: Enable development mode only when actively developing and disable it when done
2. **Specific Files**: Enable development mode only for the specific files you need to modify
3. **Audit Trail**: All changes made while development mode is enabled are still logged in the change history
4. **Team Awareness**: Inform team members when development mode is enabled to prevent conflicts

## Best Practices

1. **Enable Only When Needed**: Enable development mode only when you need to make changes to protected files
2. **Disable Promptly**: Disable development mode as soon as you're done making changes
3. **Use Specific Files**: Enable development mode for specific files rather than all files when possible
4. **Document Changes**: Document any changes made while development mode is enabled
5. **Review Changes**: Regularly review the change history to ensure all changes made while development mode was enabled were intentional

## Troubleshooting

### Common Issues

1. **Permission Denied**: If you're still getting permission denied errors after enabling development mode, try:
   - Checking if the file path is correct
   - Ensuring development mode is enabled for the correct file
   - Restarting the SigFile service

2. **Immutable Flags Not Removed**: If immutable flags are not being removed:
   - Check if you have the necessary permissions to modify file attributes
   - Try running the command with elevated privileges
   - Check the logs for any error messages

## Related Documentation
- [Permission System](permission-system.md) - The role-based permission system
- [Security Best Practices](security-best-practices.md) - General security guidelines
- [Audit Logging](audit-logging.md) - How changes are logged and monitored 