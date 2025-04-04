# Permission System Documentation

## Overview
SigFile implements a comprehensive role-based permission system to ensure secure and controlled access to development resources.

## Roles and Permissions

### Role Definitions

1. **ADMIN**
   - Full system access
   - Can modify all permissions
   - Has immutable permissions by default
   - Can enable/disable god mode

2. **USER**
   - Standard development access
   - Can read and write to project files
   - Cannot modify system settings
   - Cannot change permissions

3. **AI_AGENT**
   - Limited automated access
   - Can read project files
   - Can write to specific directories
   - Cannot modify permissions

4. **SYSTEM**
   - Internal system operations
   - Automatic file tracking
   - Log management
   - Backup operations

### Permission Types

1. **read**
   - View files and documentation
   - Access project history
   - View system logs

2. **write**
   - Modify files and documentation
   - Create new files
   - Update existing content

3. **execute**
   - Run commands and scripts
   - Execute system operations
   - Perform backups

4. **immutable**
   - Set files as read-only
   - Prevent modifications
   - Protect critical files

## Managing Permissions

### Command Line Interface

```bash
# Enable god mode (all permissions)
sigfile devenv permissions --god-mode --on

# Disable god mode
sigfile devenv permissions --god-mode --off

# Set specific role permissions
sigfile devenv permissions --role admin --permission write --on
sigfile devenv permissions --role user --permission read --on

# Check current permissions
sigfile devenv permissions --status

# List all roles and their permissions
sigfile devenv permissions --list
```

### Permission States

1. **Enabled**
   - Permission is active
   - Role can perform the action
   - Default state for admin roles

2. **Disabled**
   - Permission is inactive
   - Role cannot perform the action
   - Default state for restricted roles

3. **Immutable**
   - Permission cannot be changed
   - Set for critical system files
   - Requires admin override

## Best Practices

1. **Role Assignment**
   - Assign minimum required permissions
   - Use admin role sparingly
   - Regularly review role assignments

2. **Permission Management**
   - Document permission changes
   - Use immutable flag for critical files
   - Monitor permission usage

3. **Security Considerations**
   - Regular permission audits
   - Monitor for unauthorized changes
   - Maintain permission logs

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Check current role
   - Verify required permissions
   - Contact admin if needed

2. **Immutable Files**
   - Verify file importance
   - Request admin override
   - Document changes

3. **Permission Changes Not Applied**
   - Check command syntax
   - Verify role permissions
   - Restart system if needed

## Related Documentation
- [Basic Usage](../getting-started/basic-usage.md)
- [Security Guide](../security/README.md)
- [CLI Reference](../api/cli.md) 