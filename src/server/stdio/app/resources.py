
"""
Area of Responsibility: Resources
- Register all @server.resource-decorated functions here.
- Resources expose files, data, or live objects to agents/LLMs via MCP.
- Use absolute URIs and document resource schemas for discoverability.
"""

import json
import tempfile
import os
import shutil
import tarfile
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path

def register_resources(server):
    """
    Register all resources with the FastMCP server instance.
    """
    @server.resource(uri="resource://hello_resource", name="Hello Resource", description="Demo resource that returns a static string.")
    def hello_resource():
        """
        Demo resource that returns a static string.
        Returns:
            str: Demo resource content.
        """
        return "Hello from the resource!"

    @server.resource(uri="resource://git_repositories", name="Git Repositories", description="List of available git repositories that can be installed.")
    def git_repositories() -> str:
        """
        Returns a JSON string containing available git repositories with metadata.
        Each repository includes name, description, URL, and installation instructions.

        Returns:
            str: JSON string with repository information
        """
        repositories = [
            {
                "name": "fastmcp-templates",
                "description": "Templates and examples for building FastMCP servers and clients",
                "url": "https://github.com/JoshuaWink/fastmcp-templates.git",
                "category": "mcp",
                "language": "python",
                "tags": ["mcp", "fastmcp", "templates", "examples"],
                "install_command": "git clone https://github.com/JoshuaWink/fastmcp-templates.git",
                "readme_url": "https://github.com/JoshuaWink/fastmcp-templates/blob/main/README.md"
            },
            {
                "name": "mcp-server-filesystem",
                "description": "MCP server for filesystem operations",
                "url": "https://github.com/modelcontextprotocol/server-filesystem.git",
                "category": "mcp",
                "language": "typescript",
                "tags": ["mcp", "filesystem", "server"],
                "install_command": "git clone https://github.com/modelcontextprotocol/server-filesystem.git",
                "readme_url": "https://github.com/modelcontextprotocol/server-filesystem/blob/main/README.md"
            },
            {
                "name": "mcp-server-git",
                "description": "MCP server for git repository operations",
                "url": "https://github.com/modelcontextprotocol/server-git.git",
                "category": "mcp",
                "language": "typescript",
                "tags": ["mcp", "git", "version-control"],
                "install_command": "git clone https://github.com/modelcontextprotocol/server-git.git",
                "readme_url": "https://github.com/modelcontextprotocol/server-git/blob/main/README.md"
            },
            {
                "name": "mcp-server-sqlite",
                "description": "MCP server for SQLite database operations",
                "url": "https://github.com/modelcontextprotocol/server-sqlite.git",
                "category": "mcp",
                "language": "typescript",
                "tags": ["mcp", "sqlite", "database"],
                "install_command": "git clone https://github.com/modelcontextprotocol/server-sqlite.git",
                "readme_url": "https://github.com/modelcontextprotocol/server-sqlite/blob/main/README.md"
            }
        ]

        return json.dumps({
            "repositories": repositories,
            "total_count": len(repositories),
            "categories": list(set(repo["category"] for repo in repositories)),
            "last_updated": "2025-01-15T10:00:00Z"
        }, indent=2)

    @server.resource(uri="resource://git_repositories/{repo_name}/download/{branch}", name="Git Repository Download", description="Download a git repository as a tar archive.")
    def download_git_repository(repo_name: str, branch: str = "main") -> bytes:
        """
        Downloads a git repository and returns it as a tar archive.

        Args:
            repo_name (str): Name of the repository to download
            branch (str): Specific branch to download (defaults to main)

        Returns:
            bytes: Tar archive of the repository
        """
        # Define allowed repositories for security
        allowed_repos = {
            "fastmcp-templates": "https://github.com/JoshuaWink/fastmcp-templates.git",
            "mcp-server-filesystem": "https://github.com/modelcontextprotocol/server-filesystem.git",
            "mcp-server-git": "https://github.com/modelcontextprotocol/server-git.git",
            "mcp-server-sqlite": "https://github.com/modelcontextprotocol/server-sqlite.git"
        }

        if repo_name not in allowed_repos:
            raise ValueError(f"Repository '{repo_name}' is not in the allowed list")

        repo_url = allowed_repos[repo_name]

        # Create temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = os.path.join(temp_dir, repo_name)

            try:
                # Clone the repository
                cmd = ['git', 'clone']
                if branch and branch != "main":
                    cmd.extend(['-b', branch])
                cmd.extend(['--depth', '1', repo_url, repo_path])  # Shallow clone for speed

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minute timeout
                )

                if result.returncode != 0:
                    raise RuntimeError(f"Failed to clone repository: {result.stderr}")

                # Create tar archive
                archive_path = os.path.join(temp_dir, f"{repo_name}.tar.gz")

                with tarfile.open(archive_path, "w:gz") as tar:
                    # Add all files from the repository
                    for root, dirs, files in os.walk(repo_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Get relative path for the archive
                            rel_path = os.path.relpath(file_path, temp_dir)
                            tar.add(file_path, arcname=rel_path)

                # Read the archive content
                with open(archive_path, 'rb') as f:
                    archive_content = f.read()

                return archive_content

            except subprocess.TimeoutExpired:
                raise RuntimeError(f"Repository download timed out for {repo_name}")
            except Exception as e:
                raise RuntimeError(f"Failed to download repository {repo_name}: {str(e)}")

    @server.resource(uri="resource://git_repositories/{repo_name}/info", name="Git Repository Info", description="Get detailed information about a git repository.")
    def git_repository_info(repo_name: str) -> str:
        """
        Returns detailed information about a git repository without downloading it.

        Args:
            repo_name (str): Name of the repository

        Returns:
            str: JSON string with repository information
        """
        # Define allowed repositories for security
        allowed_repos = {
            "fastmcp-templates": {
                "url": "https://github.com/JoshuaWink/fastmcp-templates.git",
                "description": "Templates and examples for building FastMCP servers and clients",
                "language": "python",
                "category": "mcp"
            },
            "mcp-server-filesystem": {
                "url": "https://github.com/modelcontextprotocol/server-filesystem.git",
                "description": "MCP server for filesystem operations",
                "language": "typescript",
                "category": "mcp"
            },
            "mcp-server-git": {
                "url": "https://github.com/modelcontextprotocol/server-git.git",
                "description": "MCP server for git repository operations",
                "language": "typescript",
                "category": "mcp"
            },
            "mcp-server-sqlite": {
                "url": "https://github.com/modelcontextprotocol/server-sqlite.git",
                "description": "MCP server for SQLite database operations",
                "language": "typescript",
                "category": "mcp"
            }
        }

        if repo_name not in allowed_repos:
            return json.dumps({
                "error": f"Repository '{repo_name}' is not in the allowed list",
                "available_repositories": list(allowed_repos.keys())
            })

        repo_info = allowed_repos[repo_name]
        repo_url = repo_info["url"]

        try:
            # Get repository information using git ls-remote
            result = subprocess.run(
                ['git', 'ls-remote', repo_url],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return json.dumps({
                    "name": repo_name,
                    "url": repo_url,
                    "error": f"Could not access repository: {result.stderr.strip()}",
                    **repo_info
                })

            # Parse branches and latest commit
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

            return json.dumps({
                "name": repo_name,
                "url": repo_url,
                "branches": branches,
                "latest_commit": latest_commit,
                "branch_count": len(branches),
                "default_branch": "main" if "main" in branches else ("master" if "master" in branches else branches[0] if branches else None),
                "download_available": True,
                "download_url": f"resource://git_repositories/{repo_name}/download",
                **repo_info
            })

        except subprocess.TimeoutExpired:
            return json.dumps({
                "name": repo_name,
                "url": repo_url,
                "error": "Repository info request timed out",
                **repo_info
            })
        except Exception as e:
            return json.dumps({
                "name": repo_name,
                "url": repo_url,
                "error": f"Error fetching repository info: {str(e)}",
                **repo_info
            })
