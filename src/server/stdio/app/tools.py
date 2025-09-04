
"""
Area of Responsibility: Tools
- Register all @server.tool-decorated functions here.
- Tools expose callable automation, scripting, or API logic to agents/LLMs via MCP.
- Document tool schemas and usage for discoverability.
"""

import subprocess
import os
from typing import Optional, Dict, Any
from pathlib import Path

def register_tools(server):
    @server.tool(name="echo", description="Echoes back the provided text.")
    def echo(text: str) -> dict:
        """
        Echo tool that returns the input text.
        Args:
            text (str): Text to echo.
        Returns:
            dict: {"text": echoed text}
        """
        return {"text": text}
    """
    Register all server-side tools with the FastMCP server instance.
    """
    @server.tool(name="hello_tool", description="Demo tool that returns a greeting.")
    def hello_tool(name: str = "World") -> str:
        """
        Demo tool that returns a greeting.
        Args:
            name (str): Name to greet.
        Returns:
            str: Greeting message.
        """
        return f"Hello, {name}!"

    @server.tool(name="raise_error", description="Tool that always raises an error for testing.")
    def raise_error():
        raise Exception("This is a test error from raise_error tool.")

    @server.tool(name="clone_git_repository", description="Clone a git repository to a specified directory.")
    def clone_git_repository(repository_url: str, target_directory: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Clone a git repository to the specified directory.

        Args:
            repository_url (str): The URL of the git repository to clone
            target_directory (str): The directory where the repository should be cloned
            branch (Optional[str]): Specific branch to clone (defaults to default branch)

        Returns:
            Dict[str, Any]: Result containing success status, path, and any error messages
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

    @server.tool(name="get_repository_info", description="Get information about a git repository without cloning it.")
    def get_repository_info(repository_url: str) -> Dict[str, Any]:
        """
        Fetch basic information about a git repository from its remote URL.

        Args:
            repository_url (str): The URL of the git repository

        Returns:
            Dict[str, Any]: Repository information including README, package files, etc.
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


def _get_repository_info(repo_path: str) -> Dict[str, Any]:
    """
    Get information about a cloned repository.
    """
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
