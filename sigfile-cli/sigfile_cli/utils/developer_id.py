import os
import git
from git import Repo
from .error_handling import ConfigurationError

def get_developer_id():
    """
    Get the developer's ID from git config or system login.
    Ensures consistency in developer identification.
    """
    try:
        # Try to get from git config first
        repo = Repo(os.getcwd(), search_parent_directories=True)
        git_config = repo.config_reader()
        developer_id = git_config.get_value('user', 'name')
        return developer_id
    except (git.InvalidGitRepositoryError, git.ConfigParserError):
        # Fall back to system login
        developer_id = os.getlogin()
        return developer_id
    except Exception as e:
        raise ConfigurationError(
            "Failed to determine developer ID. Please ensure git is configured or system login is available.",
            command="decision"
        ) 