# Permission Manager

The Permission Manager is a core component of SigFile that provides role-based access control for files in your project. It ensures that only authorized roles can access and modify specific files, protecting your development history from unauthorized changes.

## Overview

The Permission Manager implements a role-based permission system with four distinct roles:

1. **SYSTEM**: System processes and file watchers
2. **AI_AGENT**: AI operations and agents
3. **ADMIN**: Administrators and privileged operations
4. **USER**: Regular users and unprivileged operations

Each role has specific permissions that determine what operations they can perform on files.

## Usage

### Basic Usage

```python
from src.scripts.permission_manager import permission_manager, FileRole

# Grant a role access to a file
permission_manager.grant_role_access("path/to/file", FileRole.SYSTEM)

# Check if a role has permission to perform an operation
has_access = permission_manager.check_access("path/to/file", FileRole.SYSTEM, "write")

# Revoke a role's access to a file
permission_manager.revoke_role_access("path/to/file", FileRole.SYSTEM)
```

### Role Permissions

Each role has specific permissions:

```python
# SYSTEM role permissions
{
    'read': True,
    'write': True,
    'execute': True,
    'immutable': False
}

# AI_AGENT role permissions
{
    'read': True,
    'write': True,
    'execute': True,
    'immutable': False
}

# ADMIN role permissions
{
    'read': True,
    'write': True,
    'execute': True,
    'immutable': True
}

# USER role permissions
{
    'read': True,
    'write': False,
    'execute': False,
    'immutable': True
}
```

### Elevating Permissions

For special operations, you can temporarily elevate permissions:

```python
# Elevate permissions for a role
permission_manager.elevate_permissions("path/to/file", FileRole.SYSTEM)

# Perform operations that require elevated permissions
# ...

# Permissions will automatically revert after the elevation timeout (default: 5 minutes)
```

## API Reference

### `grant_role_access(file_path, role)`

Grants a role access to a file.

**Parameters:**
- `file_path` (str): Path to the file
- `role` (FileRole): Role to grant access to

**Returns:**
- `bool`: True if access was granted, False otherwise

### `revoke_role_access(file_path, role)`

Revokes a role's access to a file.

**Parameters:**
- `file_path` (str): Path to the file
- `role` (FileRole): Role to revoke access from

**Returns:**
- `bool`: True if access was revoked, False otherwise

### `elevate_permissions(file_path, role)`

Temporarily elevates permissions for a role.

**Parameters:**
- `file_path` (str): Path to the file
- `role` (FileRole): Role to elevate permissions for

**Returns:**
- `bool`: True if permissions were elevated, False otherwise

### `check_access(file_path, role, operation)`

Checks if a role has permission to perform an operation on a file.

**Parameters:**
- `file_path` (str): Path to the file
- `role` (FileRole): Role to check access for
- `operation` (str): Operation to check ('read', 'write', 'execute', 'immutable')

**Returns:**
- `bool`: True if the role has permission, False otherwise

## Best Practices

1. **Principle of Least Privilege**: Grant only the permissions necessary for each role to perform its tasks.
2. **Regular Audits**: Periodically review and update permissions to ensure they remain appropriate.
3. **Documentation**: Document all permission changes and their rationale.
4. **Monitoring**: Monitor permission changes for unusual patterns or unauthorized modifications.

## Related Documentation
- [Permission System](permission-system.md) - Overview of the role-based permission system
- [Security Best Practices](security-best-practices.md) - General security guidelines
- [Audit Logging](audit-logging.md) - How permission changes are logged and monitored 