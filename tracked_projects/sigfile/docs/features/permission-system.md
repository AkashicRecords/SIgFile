# Permission System

SigFile implements a role-based permission system to protect your development history. This system provides granular control over file access and modifications, ensuring that only authorized roles can make changes to specific files.

## Overview

The permission system is based on four distinct roles, each with specific permissions and access levels. Files can be accessed by multiple roles simultaneously, with the most permissive access level being applied.

## Roles and Permissions

### 1. SYSTEM Role
- **Access Level**: Full access to all files
- **Capabilities**:
  - Can modify any file
  - Cannot make files immutable
  - Used by system processes and file watchers
- **Use Cases**:
  - File system monitoring
  - Automated backups
  - System-level operations

### 2. AI_AGENT Role
- **Access Level**: Full access to AI-related directories
- **Capabilities**:
  - Can modify files in ai_conversations, thinking, and changes directories
  - Cannot make files immutable
  - Used by AI operations and agents
- **Use Cases**:
  - AI-assisted code generation
  - Documentation updates
  - Code analysis

### 3. ADMIN Role
- **Access Level**: Full access to all files
- **Capabilities**:
  - Can make files immutable
  - Can temporarily elevate permissions
  - Can modify any file
  - Used by administrators and privileged operations
- **Use Cases**:
  - System configuration
  - Permission management
  - Security operations

### 4. USER Role
- **Access Level**: Read-only access to all files
- **Capabilities**:
  - Cannot modify or delete files
  - Files appear immutable to users
  - Used by regular users and unprivileged operations
- **Use Cases**:
  - Viewing documentation
  - Reading code
  - Accessing project resources

## Permission Management

### Granting Access
To grant a role access to a file:

```python
from src.scripts.permission_manager import permission_manager, FileRole

# Grant SYSTEM role access to a file
permission_manager.grant_role_access("path/to/file", FileRole.SYSTEM)
```

### Revoking Access
To revoke a role's access to a file:

```python
# Revoke SYSTEM role access to a file
permission_manager.revoke_role_access("path/to/file", FileRole.SYSTEM)
```

### Elevating Permissions
To temporarily elevate permissions for a role:

```python
# Elevate permissions for SYSTEM role
permission_manager.elevate_permissions("path/to/file", FileRole.SYSTEM)
```

## Permission Changes

All permission changes are logged in the change history with:
- The file path
- The role making the change
- The type of change (grant/revoke)
- The context of the change
- Timestamp

This ensures a complete audit trail of all permission modifications.

## Best Practices

1. **Principle of Least Privilege**: Grant only the permissions necessary for each role to perform its tasks.
2. **Regular Audits**: Periodically review and update permissions to ensure they remain appropriate.
3. **Documentation**: Document all permission changes and their rationale.
4. **Monitoring**: Monitor permission changes for unusual patterns or unauthorized modifications.

## Related Documentation
- [Development Mode](development-mode.md) - How to bypass permission restrictions during development
- [Security Best Practices](security-best-practices.md) - General security guidelines
- [Audit Logging](audit-logging.md) - How permission changes are logged and monitored 