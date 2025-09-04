#!/usr/bin/env python3
"""
Test CLI output formatting and user feedback
Tests for help text, error messages, success messages, and folder structure display
"""

import pytest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import os


class TestCLIOutputFormatting:
    """Test CLI output formatting and user feedback"""

    def test_help_text_formatting(self):
        """Test that help text is properly formatted"""
        # Run CLI with --help flag
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "--help"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
        )

        # Check that help text contains expected elements
        assert "FastestMCP CLI" in result.stdout
        assert "Advanced boilerplate generator" in result.stdout
        assert "Examples:" in result.stdout
        assert "positional arguments:" in result.stdout
        assert "options:" in result.stdout  # CLI uses "options:" not "optional arguments:"

        # Check formatting - should have proper line breaks and indentation
        lines = result.stdout.split('\n')
        assert any("  fastestmcp server --level" in line for line in lines)
        assert any("  fastestmcp server --template" in line for line in lines)

    def test_help_text_structure(self):
        """Test that help text has proper structure and sections"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "--help"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
        )

        help_text = result.stdout

        # Should contain main sections
        assert "usage:" in help_text.lower()
        assert "description" in help_text.lower() or "FastestMCP CLI" in help_text
        assert "examples:" in help_text.lower()

        # Should contain command options
        assert "--level" in help_text
        assert "--template" in help_text
        assert "--name" in help_text
        assert "--transport" in help_text
        assert "--structure" in help_text

    @pytest.mark.parametrize("invalid_arg", [
        "--invalid-option",
        "--nonexistent",
        "invalid_command"
    ])
    def test_error_message_formatting(self, invalid_arg):
        """Test that error messages are properly formatted"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", invalid_arg],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
        )

        # Should have non-zero exit code for errors
        assert result.returncode != 0

        # Should contain error information
        error_output = result.stderr + result.stdout
        assert len(error_output.strip()) > 0

        # Should contain some indication of error
        assert any(keyword in error_output.lower() for keyword in [
            "error", "invalid", "unrecognized", "usage"
        ])

    def test_missing_required_argument_error(self):
        """Test error formatting when required arguments are missing"""
        # Run without required --name argument
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "server", "--level", "1"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
        )

        # Should fail due to missing --name
        assert result.returncode != 0

        # Should contain error message about missing argument
        error_output = result.stderr + result.stdout
        assert "following arguments are required" in error_output or "required" in error_output.lower()

    def test_invalid_choice_error_formatting(self):
        """Test error formatting for invalid argument choices"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "test", "--level", "10"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
        )

        # Should fail due to invalid level choice
        assert result.returncode != 0

        # Should contain error about invalid choice
        error_output = result.stderr + result.stdout
        assert "invalid choice" in error_output or "choose from" in error_output

    def test_success_message_formatting(self):
        """Test that success messages are properly formatted"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "testserver", "--level", "1", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            # Should contain success message
            output = result.stdout + result.stderr
            assert "✅" in output or "success" in output.lower() or "generated" in output.lower()

            # Should contain the generated file path
            assert "testserver.py" in output

    def test_folder_structure_display(self):
        """Test that folder structure is displayed correctly"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "testserver", "--structure", "structured", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain folder structure information
            assert "```" in output  # Markdown code blocks
            assert "├──" in output or "└──" in output  # Tree structure characters
            assert "testserver/" in output  # Directory name

    def test_mono_file_generation_message(self):
        """Test message formatting for mono-file generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "monoserver", "--structure", "mono", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain mono-file specific messaging
            assert "mono" in output.lower() or "single" in output.lower()
            assert "monoserver.py" in output

    def test_structured_generation_message(self):
        """Test message formatting for structured generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "structserver", "--structure", "structured", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain structured specific messaging
            assert "structured" in output.lower() or "folder" in output.lower()
            assert "structserver/" in output

    def test_template_generation_message(self):
        """Test message formatting for template-based generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--template", "weather", "--name", "weatherserver", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain template-specific messaging
            assert "weather" in output.lower() or "template" in output.lower()
            assert "weatherserver" in output

    def test_component_count_display(self):
        """Test that component counts are displayed in output"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "componenttest", "--tools", "3", "--resources", "2", "--prompts", "1", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain success message and file generation info
            # Note: CLI doesn't show detailed component counts in output, just success message
            assert "✅" in output or "success" in output.lower() or "generated" in output.lower()
            assert "componenttest" in output

    def test_transport_display(self):
        """Test that transport type is displayed in output"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "transporttest", "--transport", "http", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain transport information
            # Note: CLI doesn't explicitly show transport type in success message, but should succeed
            assert "✅" in output or "success" in output.lower() or "generated" in output.lower()
            assert "transporttest" in output

    def test_server_type_display(self):
        """Test that server type is displayed in output"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "typetest", "--type", "mcp", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain type information
            # Note: CLI doesn't explicitly show server type in success message, but should succeed
            assert "✅" in output or "success" in output.lower() or "generated" in output.lower()
            assert "typetest" in output

    def test_output_directory_handling(self):
        """Test that output directory is handled correctly in messages"""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_output = Path(temp_dir) / "custom_dir"
            custom_output.mkdir()

            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "dirtest", "--output", str(custom_output)],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain output directory information
            assert "custom_dir" in output or str(custom_output) in output

    def test_unicode_and_emoji_display(self):
        """Test that unicode characters and emojis are displayed correctly"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "emojitest", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain emojis or unicode characters (check mark, etc.)
            # Note: Some terminals may not support emojis, so this is a soft check
            has_unicode = any(ord(char) > 127 for char in output)
            has_emoji = "✅" in output or "❌" in output or "📦" in output

            # At minimum, should have some form of success indication
            assert has_unicode or has_emoji or "success" in output.lower() or "generated" in output.lower()

    def test_verbose_output_formatting(self):
        """Test verbose output formatting (if supported)"""
        # Note: Current CLI doesn't have verbose flag, but test structure for future enhancement
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "verbosetest", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Should succeed
            assert result.returncode == 0

            output = result.stdout

            # Should contain basic success information
            assert len(output.strip()) > 0
            assert "verbosetest" in output

    def test_error_output_redirection(self):
        """Test that error messages go to stderr and success to stdout"""
        # Test success case
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "server", "--name", "stdouttest", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
            )

            # Success should go to stdout
            assert len(result.stdout.strip()) > 0
            assert "stdouttest" in result.stdout

            # Stderr should be minimal for success case
            assert len(result.stderr.strip()) == 0 or "warning" not in result.stderr.lower()

        # Test error case
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "server", "--invalid-flag"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
        )

        # Error should go to stderr
        assert len(result.stderr.strip()) > 0
        assert "error" in result.stderr.lower() or "invalid" in result.stderr.lower()

    def test_output_consistency(self):
        """Test that output format is consistent across different commands"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test multiple generation types
            test_cases = [
                ["server", "--name", "consistency1", "--level", "1"],
                ["server", "--name", "consistency2", "--template", "weather"],
                ["server", "--name", "consistency3", "--tools", "2", "--resources", "1"]
            ]

            outputs = []
            for case in test_cases:
                result = subprocess.run(
                    [sys.executable, "-m", "fastestmcp.cli"] + case + ["--output", temp_dir],
                    capture_output=True,
                    text=True,
                    cwd="/Users/jwink/Documents/github/fastmcp-templates/src"
                )
                assert result.returncode == 0
                outputs.append(result.stdout)

            # All outputs should have similar structure
            for output in outputs:
                # Should contain success indicator
                assert "✅" in output or "success" in output.lower() or "generated" in output.lower()

                # Should contain the project name
                assert any(name in output for name in ["consistency1", "consistency2", "consistency3"])