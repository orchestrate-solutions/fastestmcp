import pytest
import tempfile
import os
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the functions directly from the module
import sys
sys.path.append('/Users/jwink/Documents/github/fastestmcp/server/stdio')

# We'll test the functions by creating them directly
def create_clone_git_repository():
    """Create the clone_git_repository function for testing."""
    import subprocess
    import os
    import json
    from typing import Optional, Dict, Any
    from pathlib import Path

    def _get_repository_info(repo_path: str) -> Dict[str, Any]:
        """Get information about a cloned repository."""
        try:
            # Get git log info
            result = subprocess.run(
                ['git', 'log', '--oneline', '-5'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )

            commits = result.stdout.strip().split('\n') if result.returncode == 0 else []

            # Get current branch
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )

            current_branch = result.stdout.strip() if result.returncode == 0 else "unknown"

            # Check for common project files
            project_files = {}
            common_files = ['README.md', 'package.json', 'requirements.txt', 'setup.py', 'pyproject.toml']

            for file in common_files:
                if os.path.exists(os.path.join(repo_path, file)):
                    project_files[file] = True

            return {
                "current_branch": current_branch,
                "recent_commits": commits,
                "project_files": project_files,
                "has_readme": project_files.get('README.md', False)
            }

        except Exception as e:
            return {
                "error": f"Could not get repository info: {str(e)}"
            }

    def clone_git_repository(repository_url: str, target_directory: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Clone a git repository to the specified directory.
        """
        try:
            # Validate inputs
            if not repository_url or not repository_url.startswith(('http', 'https', 'git@', 'ssh://')):
                return {
                    "success": False,
                    "error": "Invalid repository URL. Must be a valid git URL.",
                    "repository_url": repository_url
                }

            # Convert target_directory to absolute path
            target_path = Path(target_directory).resolve()

            # Check if target directory already exists and is not empty
            if target_path.exists() and any(target_path.iterdir()):
                return {
                    "success": False,
                    "error": f"Target directory '{target_directory}' already exists and is not empty.",
                    "target_directory": target_directory
                }

            # Create parent directories if they don't exist
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # Prepare git clone command
            cmd = ['git', 'clone']
            if branch:
                cmd.extend(['-b', branch])
            cmd.extend([repository_url, str(target_path)])

            # Execute git clone
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                # Get repository info
                repo_info = _get_repository_info(str(target_path))

                return {
                    "success": True,
                    "message": f"Successfully cloned repository to {target_directory}",
                    "repository_url": repository_url,
                    "target_directory": target_directory,
                    "branch": branch or "default",
                    "repository_info": repo_info
                }
            else:
                return {
                    "success": False,
                    "error": f"Git clone failed: {result.stderr.strip()}",
                    "repository_url": repository_url,
                    "target_directory": target_directory,
                    "return_code": result.returncode
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Git clone operation timed out after 5 minutes",
                "repository_url": repository_url,
                "target_directory": target_directory
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error during git clone: {str(e)}",
                "repository_url": repository_url,
                "target_directory": target_directory
            }

    return clone_git_repository

def create_get_repository_info():
    """Create the get_repository_info function for testing."""
    import subprocess
    from typing import Dict, Any

    def get_repository_info(repository_url: str) -> Dict[str, Any]:
        """
        Fetch basic information about a git repository from its remote URL.
        """
        try:
            # Use git ls-remote to get basic info without cloning
            result = subprocess.run(
                ['git', 'ls-remote', repository_url],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Could not access repository: {result.stderr.strip()}",
                    "repository_url": repository_url
                }

            # Parse the output to get branches and commit info
            lines = result.stdout.strip().split('\n')
            branches = []
            latest_commit = None

            for line in lines:
                if line:
                    commit_hash, ref = line.split('\t')
                    if ref.startswith('refs/heads/'):
                        branch_name = ref.replace('refs/heads/', '')
                        branches.append(branch_name)
                    elif ref == 'HEAD':
                        latest_commit = commit_hash

            return {
                "success": True,
                "repository_url": repository_url,
                "branches": branches,
                "latest_commit": latest_commit,
                "branch_count": len(branches),
                "default_branch": "main" if "main" in branches else ("master" if "master" in branches else branches[0] if branches else None)
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Repository info request timed out",
                "repository_url": repository_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error fetching repository info: {str(e)}",
                "repository_url": repository_url
            }

    return get_repository_info


class TestGitTools:
    """Test cases for git repository tools."""

    def setup_method(self):
        """Set up test fixtures."""
        self.clone_git_repository = create_clone_git_repository()
        self.get_repository_info = create_get_repository_info()

    def test_clone_git_repository_success(self):
        """Test successful git repository cloning."""
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = os.path.join(temp_dir, "test_repo")

            # Mock subprocess.run for successful clone
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                result = self.clone_git_repository(
                    repository_url="https://github.com/example/test-repo.git",
                    target_directory=target_path
                )

                assert result["success"] is True
                assert "Successfully cloned repository" in result["message"]
                assert result["repository_url"] == "https://github.com/example/test-repo.git"
                assert result["target_directory"] == target_path

    def test_clone_git_repository_invalid_url(self):
        """Test cloning with invalid repository URL."""
        result = self.clone_git_repository(
            repository_url="invalid-url",
            target_directory="/tmp/test"
        )

        assert result["success"] is False
        assert "Invalid repository URL" in result["error"]

    def test_clone_git_repository_directory_exists(self):
        """Test cloning when target directory already exists and is not empty."""
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = os.path.join(temp_dir, "existing_dir")
            os.makedirs(target_path)
            # Create a file in the directory
            with open(os.path.join(target_path, "test.txt"), "w") as f:
                f.write("test")

            result = self.clone_git_repository(
                repository_url="https://github.com/example/test-repo.git",
                target_directory=target_path
            )

            assert result["success"] is False
            assert "already exists and is not empty" in result["error"]

    def test_clone_git_repository_git_failure(self):
        """Test handling of git command failure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = os.path.join(temp_dir, "test_repo")

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(
                    returncode=128,
                    stdout="",
                    stderr="fatal: repository not found"
                )

                result = self.clone_git_repository(
                    repository_url="https://github.com/nonexistent/repo.git",
                    target_directory=target_path
                )

                assert result["success"] is False
                assert "Git clone failed" in result["error"]
                assert "repository not found" in result["error"]

    def test_clone_git_repository_timeout(self):
        """Test handling of git clone timeout."""
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = os.path.join(temp_dir, "test_repo")

            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.TimeoutExpired(
                    cmd=['git', 'clone', 'https://github.com/example/repo.git', target_path],
                    timeout=300
                )

                result = self.clone_git_repository(
                    repository_url="https://github.com/example/repo.git",
                    target_directory=target_path
                )

                assert result["success"] is False
                assert "timed out" in result["error"]

    def test_get_repository_info_success(self):
        """Test successful repository info retrieval."""
        mock_output = """abc123456789\trefs/heads/main
def789012345\trefs/heads/develop
ghi012345678\tHEAD
"""

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout=mock_output,
                stderr=""
            )

            result = self.get_repository_info("https://github.com/example/repo.git")

            assert result["success"] is True
            assert result["repository_url"] == "https://github.com/example/repo.git"
            assert "main" in result["branches"]
            assert "develop" in result["branches"]
            assert result["default_branch"] == "main"
            assert result["latest_commit"] == "ghi012345678"

    def test_get_repository_info_invalid_repo(self):
        """Test repository info retrieval for invalid repository."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=128,
                stdout="",
                stderr="fatal: repository not found"
            )

            result = self.get_repository_info("https://github.com/nonexistent/repo.git")

            assert result["success"] is False
            assert "Could not access repository" in result["error"]

    def test_get_repository_info_timeout(self):
        """Test repository info retrieval timeout."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(
                cmd=['git', 'ls-remote', 'https://github.com/example/repo.git'],
                timeout=30
            )

            result = self.get_repository_info("https://github.com/example/repo.git")

            assert result["success"] is False
            assert "timed out" in result["error"]

    def test_clone_with_branch(self):
        """Test cloning a specific branch."""
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = os.path.join(temp_dir, "test_repo")

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                result = self.clone_git_repository(
                    repository_url="https://github.com/example/test-repo.git",
                    target_directory=target_path,
                    branch="develop"
                )

                assert result["success"] is True
                assert result["branch"] == "develop"

                # Verify git clone was called with branch option
                # The function makes 3 calls: clone, log, and branch
                assert mock_run.call_count == 3

                # Check the first call (git clone) has the branch option
                clone_call_args = mock_run.call_args_list[0][0][0]
                assert '-b' in clone_call_args
                assert 'develop' in clone_call_args