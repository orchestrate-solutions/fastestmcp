import pytest
import tempfile
import subprocess
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import argparse


class TestCLICommands:
    """Test CLI command functionality"""

    def test_cli_help_output(self):
        """Test that CLI shows help when no arguments provided"""
        result = subprocess.run([
            sys.executable, "-m", "fastestmcp.cli"
        ], capture_output=True, text=True, cwd="/Users/jwink/Documents/github/fastestmcp/src")

        assert result.returncode == 0
        assert "FastestMCP CLI" in result.stdout
        assert "Available commands" in result.stdout
        assert "new" in result.stdout
        assert "client" in result.stdout

    def test_cli_new_help(self):
        """Test CLI new command help"""
        result = subprocess.run([
            sys.executable, "-m", "fastestmcp.cli", "new", "--help"
        ], capture_output=True, text=True, cwd="/Users/jwink/Documents/github/fastestmcp/src")

        assert result.returncode == 0
        assert "--level" in result.stdout
        assert "--template" in result.stdout
        assert "--name" in result.stdout
        assert "--tools" in result.stdout
        assert "--transport" in result.stdout

    def test_cli_client_help(self):
        """Test CLI client command help"""
        result = subprocess.run([
            sys.executable, "-m", "fastestmcp.cli", "client", "--help"
        ], capture_output=True, text=True, cwd="/Users/jwink/Documents/github/fastestmcp/src")

        assert result.returncode == 0
        assert "--template" in result.stdout
        assert "--name" in result.stdout
        assert "--apis" in result.stdout
        assert "--transport" in result.stdout

    def test_cli_new_level_1_generation(self):
        """Test CLI new command with level 1 generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "new",
                "--level", "1", "--name", "test_cli_level1"
            ], capture_output=True, text=True, cwd=temp_dir,
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout
            assert "Level 1 boilerplate generated" in result.stdout

            # Check that file was created
            generated_file = Path(temp_dir) / "test_cli_level1.py"
            assert generated_file.exists()

    def test_cli_new_level_2_generation(self):
        """Test CLI new command with level 2 generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "new",
                "--level", "2", "--name", "test_cli_level2"
            ], capture_output=True, text=True, cwd=temp_dir,
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout
            assert "Level 2 boilerplate generated" in result.stdout

            # Check that file was created
            generated_file = Path(temp_dir) / "test_cli_level2.py"
            assert generated_file.exists()

    def test_cli_new_custom_generation(self):
        """Test CLI new command with custom parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "new",
                "--name", "test_custom", "--tools", "3", "--resources", "2",
                "--prompts", "1", "--transport", "stdio", "--structure", "mono"
            ], capture_output=True, text=True, cwd=temp_dir,
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout

            # Check that file was created
            generated_file = Path(temp_dir) / "test_custom.py"
            assert generated_file.exists()

    def test_cli_new_with_notifications_subscriptions(self):
        """Test CLI new command with notification and subscription parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "new",
                "--name", "test_notifications", "--tools", "2", "--resources", "1",
                "--notifications", "3", "--subscriptions", "2", "--transport", "stdio", "--structure", "mono"
            ], capture_output=True, text=True, cwd=temp_dir,
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout

            # Check that file was created
            generated_file = Path(temp_dir) / "test_notifications.py"
            assert generated_file.exists()

            # Verify MCP-compliant server code is present (new component system)
            content = generated_file.read_text()
            assert "register_component" in content
            assert "register_notifications" in content
            assert "register_subscriptions" in content
            assert "count=3" in content  # 3 notifications
            assert "count=2" in content  # 2 subscriptions

            # Verify no old decorator patterns
            assert "@server.subscription" not in content  # Old pattern removed

    def test_cli_client_with_notifications_subscriptions(self):
        """Test CLI client command with notification and subscription parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "client",
                "--name", "test_client_notifications", "--apis", "2", "--integrations", "1",
                "--notifications", "2", "--subscriptions", "1", "--transport", "stdio", "--structure", "mono"
            ], capture_output=True, text=True, cwd=temp_dir,
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout

            # Check that file was created
            generated_file = Path(temp_dir) / "test_client_notifications_client.py"
            assert generated_file.exists()

            # Verify MCP-compliant client code is present
            content = generated_file.read_text()
            assert "Test_Client_NotificationsClient" in content
            assert "list_tools" in content
            assert "call_tool" in content
            assert "send_log" in content
            assert "request_elicitation" in content
            assert "request_sampling" in content

            # Verify no old non-MCP patterns
            assert "add_notification" not in content  # Old pattern removed
            assert "subscribe" not in content  # Old pattern removed
            assert "unsubscribe" not in content  # Old pattern removed

    def test_cli_new_structured_generation(self):
        """Test CLI new command with structured generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "new",
                "--name", "test_structured", "--tools", "2", "--resources", "1",
                "--structure", "structured"
            ], capture_output=True, text=True, cwd=temp_dir,
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout

            # Check that directory was created
            generated_dir = Path(temp_dir) / "test_structured"
            assert generated_dir.exists()
            assert generated_dir.is_dir()

    def test_cli_new_invalid_level(self):
        """Test CLI new command with invalid level"""
        result = subprocess.run([
            sys.executable, "-m", "fastestmcp.cli", "new",
            "--level", "99", "--name", "test_invalid"
        ], capture_output=True, text=True, cwd="/tmp",
        env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

        assert result.returncode == 2  # argparse validation error
        assert "invalid choice: 99" in result.stderr

    def test_cli_new_missing_name(self):
        """Test CLI new command with missing required name"""
        result = subprocess.run([
            sys.executable, "-m", "fastestmcp.cli", "new",
            "--level", "1"
        ], capture_output=True, text=True, cwd="/tmp",
        env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

        assert result.returncode == 2  # argparse error
        assert "the following arguments are required: --name" in result.stderr

    def test_cli_new_template_generation(self):
        """Test CLI new command with template"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "new",
                "--template", "weather", "--name", "test_weather"
            ], capture_output=True, text=True, cwd=temp_dir,
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout
            assert "Template 'weather' server generated" in result.stdout

            # Check that file was created
            generated_file = Path(temp_dir) / "test_weather.py"
            assert generated_file.exists()

    def test_cli_client_custom_generation(self):
        """Test CLI client command with custom parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "client",
                "--name", "test_client", "--apis", "2", "--integrations", "1",
                "--transport", "stdio", "--structure", "mono"
            ], capture_output=True, text=True, cwd=temp_dir,
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout

            # Check that file was created
            generated_file = Path(temp_dir) / "test_client_client.py"
            assert generated_file.exists()

    def test_cli_client_missing_name(self):
        """Test CLI client command with missing required name"""
        result = subprocess.run([
            sys.executable, "-m", "fastestmcp.cli", "client",
            "--apis", "2"
        ], capture_output=True, text=True, cwd="/tmp",
        env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

        assert result.returncode == 2  # argparse error
        assert "the following arguments are required: --name" in result.stderr

    def test_cli_invalid_command(self):
        """Test CLI with invalid command"""
        result = subprocess.run([
            sys.executable, "-m", "fastestmcp.cli", "invalid_command"
        ], capture_output=True, text=True, cwd="/tmp",
        env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

        assert result.returncode == 2  # argparse error
        assert "invalid choice: 'invalid_command'" in result.stderr

    def test_cli_new_output_directory(self):
        """Test CLI new command with custom output directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_output = Path(temp_dir) / "custom_dir"
            custom_output.mkdir()

            result = subprocess.run([
                sys.executable, "-m", "fastestmcp.cli", "new",
                "--level", "1", "--name", "test_output", "--output", str(custom_output)
            ], capture_output=True, text=True, cwd="/tmp",
            env={**os.environ, "PYTHONPATH": "/Users/jwink/Documents/github/fastestmcp/src"})

            assert result.returncode == 0
            assert "✅" in result.stdout

            # Check that file was created in custom directory
            generated_file = custom_output / "test_output.py"
            assert generated_file.exists()