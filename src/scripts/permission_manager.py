import os
import stat
import subprocess
import sys
import logging
from enum import Enum
from typing import List, Set
import time
import getpass

logger = logging.getLogger(__name__)

class PermissionError(Exception):
    """Custom exception for permission-related errors."""
    def __init__(self, message: str, role: str = None, file_path: str = None):
        self.message = message
        self.role = role
        self.file_path = file_path
        super().__init__(self.message)

class FileRole(Enum):
    """Roles that can access and modify files."""
    SYSTEM = "system"  # System service worker
    AI_AGENT = "ai_agent"  # AI agent worker
    ADMIN = "admin"  # Administrative access
    USER = "user"  # Regular user access

class PermissionManager:
    def __init__(self):
        self.role_permissions = {
            FileRole.SYSTEM: {
                'read': True,
                'write': True,
                'execute': True,
                'immutable': False
            },
            FileRole.AI_AGENT: {
                'read': True,
                'write': True,
                'execute': True,
                'immutable': False
            },
            FileRole.ADMIN: {
                'read': True,
                'write': True,
                'execute': True,
                'immutable': True
            },
            FileRole.USER: {
                'read': True,
                'write': False,
                'execute': False,
                'immutable': True
            }
        }
        
        # Track which roles have access to which files
        self.file_roles: dict[str, Set[FileRole]] = {}
        
        # Track elevated permissions with timestamps
        self.elevated_permissions: dict[str, float] = {}
        self.elevation_timeout = 300  # 5 minutes
        
        # Cache for permission checks
        self.permission_cache: dict[str, dict] = {}
        self.cache_timeout = 60  # 1 minute
        
        # Development mode flag
        self.dev_mode = False
        self.dev_mode_files = set()
        
        # Store original permissions for restoration
        self.original_permissions = {}
        
        # Venv restriction flag
        self.venv_restricted = False
        self.venv_restricted_files = set()
        
        # Track venv bypass confirmations
        self.venv_bypass_confirmations = set()
    
    def enable_dev_mode(self, file_path: str = None):
        """Enable development mode for a specific file or all files."""
        try:
            self.dev_mode = True
            if file_path:
                self.dev_mode_files.add(file_path)
                self._store_original_permissions(file_path)
                self._make_writable(file_path)
            logger.info(f"Development mode enabled for {'all files' if file_path is None else file_path}")
        except Exception as e:
            logger.error(f"Error enabling development mode: {str(e)}")
            raise

    def disable_dev_mode(self, file_path: str = None):
        """Disable development mode for a specific file or all files."""
        try:
            if file_path:
                self.dev_mode_files.discard(file_path)
                if not self.dev_mode_files:
                    self.dev_mode = False
                self._restore_original_permissions(file_path)
            else:
                self.dev_mode = False
                for path in list(self.dev_mode_files):
                    self._restore_original_permissions(path)
                self.dev_mode_files.clear()
            logger.info(f"Development mode disabled for {'all files' if file_path is None else file_path}")
        except Exception as e:
            logger.error(f"Error disabling development mode: {str(e)}")
            raise

    def _store_original_permissions(self, file_path: str):
        """Store the original permissions of a file."""
        try:
            if os.path.exists(file_path):
                self.original_permissions[file_path] = {
                    'mode': os.stat(file_path).st_mode,
                    'uid': os.stat(file_path).st_uid,
                    'gid': os.stat(file_path).st_gid
                }
        except Exception as e:
            logger.error(f"Error storing original permissions: {str(e)}")
            raise

    def _make_writable(self, file_path: str):
        """Make a file writable using standard permissions."""
        try:
            if os.path.exists(file_path):
                # Get current user's uid and gid
                current_uid = os.getuid()
                current_gid = os.getgid()
                
                # Set ownership to current user
                os.chown(file_path, current_uid, current_gid)
                
                # Set permissions to user read-write, group read
                os.chmod(file_path, 0o644)
                
                logger.info(f"Made file writable: {file_path}")
        except Exception as e:
            logger.error(f"Error making file writable: {str(e)}")
            raise

    def _restore_original_permissions(self, file_path: str):
        """Restore the original permissions of a file."""
        try:
            if file_path in self.original_permissions:
                orig = self.original_permissions[file_path]
                os.chown(file_path, orig['uid'], orig['gid'])
                os.chmod(file_path, orig['mode'])
                del self.original_permissions[file_path]
                logger.info(f"Restored original permissions for: {file_path}")
        except Exception as e:
            logger.error(f"Error restoring original permissions: {str(e)}")
            raise

    def grant_role_access(self, file_path: str, role: FileRole) -> bool:
        """Grant a role access to a file."""
        try:
            if file_path not in self.file_roles:
                self.file_roles[file_path] = set()
            self.file_roles[file_path].add(role)
            
            # Apply basic permissions
            self._apply_basic_permissions(file_path, role)
            return True
        except Exception as e:
            logger.error(f"Failed to grant role access: {str(e)}")
            return False
    
    def revoke_role_access(self, file_path: str, role: FileRole) -> bool:
        """Revoke a role's access to a file."""
        try:
            if file_path in self.file_roles and role in self.file_roles[file_path]:
                self.file_roles[file_path].remove(role)
                self._update_file_permissions(file_path)
            return True
        except Exception as e:
            logger.error(f"Failed to revoke role access: {str(e)}")
            return False
    
    def elevate_permissions(self, file_path: str, role: FileRole) -> bool:
        """Temporarily elevate permissions for a role."""
        try:
            if role in [FileRole.SYSTEM, FileRole.ADMIN]:
                self.elevated_permissions[file_path] = time.time()
                os.chmod(file_path, 0o666)  # Make writable
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to elevate permissions: {str(e)}")
            return False
    
    def _apply_basic_permissions(self, file_path: str, role: FileRole):
        """Apply basic file permissions without system commands."""
        perms = self.role_permissions[role]
        
        # Get current permissions
        current_mode = os.stat(file_path).st_mode
        
        # Calculate new permissions
        new_mode = current_mode
        if perms['read']:
            new_mode |= stat.S_IREAD
        if perms['write']:
            new_mode |= stat.S_IWRITE
        if perms['execute']:
            new_mode |= stat.S_IEXEC
        
        # Apply permissions
        os.chmod(file_path, new_mode)
    
    def _update_file_permissions(self, file_path: str):
        """Update file permissions based on current roles."""
        if file_path in self.file_roles:
            # Remove all current permissions
            if sys.platform == 'linux':
                subprocess.run(['chattr', '-i', file_path], check=True)
            elif sys.platform == 'darwin':
                subprocess.run(['chflags', 'nouchg', file_path], check=True)
            elif sys.platform == 'win32':
                subprocess.run(['attrib', '-R', '-S', '-H', file_path], check=True)
            
            # Apply permissions for each role
            for role in self.file_roles[file_path]:
                self._apply_basic_permissions(file_path, role)
    
    def enable_venv_restriction(self, file_path: str = None):
        """Enable venv restriction for a specific file or all files."""
        try:
            self.venv_restricted = True
            if file_path:
                self.venv_restricted_files.add(file_path)
            logger.info(f"Venv restriction {'enabled for file: ' + file_path if file_path else 'enabled for all files'}")
        except Exception as e:
            logger.error(f"Error enabling venv restriction: {str(e)}")
            raise

    def disable_venv_restriction(self, file_path: str = None):
        """Disable venv restriction for a specific file or all files."""
        try:
            if file_path:
                self.venv_restricted_files.discard(file_path)
                if not self.venv_restricted_files:
                    self.venv_restricted = False
            else:
                self.venv_restricted = False
                self.venv_restricted_files.clear()
            logger.info(f"Venv restriction {'disabled for file: ' + file_path if file_path else 'disabled for all files'}")
        except Exception as e:
            logger.error(f"Error disabling venv restriction: {str(e)}")
            raise

    def _handle_venv_restriction(self, file_path: str) -> bool:
        """Handle venv restriction with user prompt."""
        if not self.venv_restricted:
            return True
            
        if file_path in self.venv_bypass_confirmations:
            return True
            
        if 'VIRTUAL_ENV' in os.environ:
            venv_path = os.environ['VIRTUAL_ENV']
            print(f"\n⚠️  WARNING: Attempting to modify file from within virtual environment:")
            print(f"   Current venv: {venv_path}")
            print(f"   Target file: {file_path}")
            print("\nThis operation is restricted when running from a virtual environment.")
            print("Continuing anyway may cause unexpected behavior.")
            
            while True:
                response = input("\nContinue anyway? [Y/n]: ").lower()
                if response in ['', 'y', 'yes']:
                    self.venv_bypass_confirmations.add(file_path)
                    return True
                elif response in ['n', 'no']:
                    return False
                print("Please answer 'y' or 'n'")
        
        return True

    def check_access(self, file_path: str, role: FileRole, operation: str) -> bool:
        """Check if a role has permission to perform an operation on a file."""
        try:
            # Development mode bypass
            if self.dev_mode and (file_path in self.dev_mode_files or not self.dev_mode_files):
                return True
            
            # Check cache first
            cache_key = f"{file_path}:{role.value}:{operation}"
            if cache_key in self.permission_cache:
                cached = self.permission_cache[cache_key]
                if time.time() - cached['timestamp'] < self.cache_timeout:
                    return cached['result']
            
            # Get role permissions
            role_perm = self.role_permissions.get(role)
            if not role_perm:
                raise PermissionError(f"Invalid role: {role.value}", role.value, file_path)
            
            # Check if role has access to file
            if file_path not in self.file_roles or role not in self.file_roles[file_path]:
                raise PermissionError(
                    f"Role {role.value} does not have access to file: {file_path}",
                    role.value,
                    file_path
                )
            
            # Check venv restriction with user prompt
            if not self._handle_venv_restriction(file_path):
                raise PermissionError(
                    f"Operation blocked due to venv restriction: {file_path}",
                    role.value,
                    file_path
                )
            
            # Check operation permission
            result = role_perm.get(operation, False)
            if not result:
                raise PermissionError(
                    f"Role {role.value} does not have {operation} permission for file: {file_path}",
                    role.value,
                    file_path
                )
            
            # Cache result
            self.permission_cache[cache_key] = {
                'timestamp': time.time(),
                'result': result
            }
            
            return result
            
        except PermissionError as e:
            logger.error(f"Permission error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error checking access: {str(e)}")
            raise PermissionError(f"Unexpected error checking access: {str(e)}", role.value, file_path)
    
    def cleanup_expired_permissions(self):
        """Clean up expired elevated permissions and cache entries."""
        current_time = time.time()
        
        # Clean up elevated permissions
        expired = [path for path, timestamp in self.elevated_permissions.items() 
                  if current_time - timestamp > self.elevation_timeout]
        for path in expired:
            del self.elevated_permissions[path]
        
        # Clean up permission cache
        expired = [key for key, data in self.permission_cache.items() 
                  if current_time - data['timestamp'] > self.cache_timeout]
        for key in expired:
            del self.permission_cache[key]

# Global permission manager instance
permission_manager = PermissionManager() 