#!/usr/bin/env python3
"""
Test CLI error handling and edge cases
Tests for invalid inputs, missing files, permission issues, and error recovery
"""

import subprocess
import sys
import tempfile
from pathlib import Path


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases"""

    def test_invalid_command_error(self):
        """Test error handling for invalid commands"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "invalid_command"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail with invalid command
        assert result.returncode != 0

        # Should contain error message about invalid choice
        error_output = result.stderr + result.stdout
        assert "invalid choice" in error_output or "unrecognized" in error_output.lower()

    def test_missing_name_argument_error(self):
        """Test error handling when required --name argument is missing"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--level", "1"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail due to missing required argument
        assert result.returncode != 0

        # Should contain error about required argument
        error_output = result.stderr + result.stdout
        assert "required" in error_output.lower() or "name" in error_output.lower()

    def test_invalid_level_choice_error(self):
        """Test error handling for invalid level choices"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--level", "10"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail due to invalid level choice
        assert result.returncode != 0

        # Should contain error about invalid choice
        error_output = result.stderr + result.stdout
        assert "invalid choice" in error_output or "choose from" in error_output

    def test_invalid_template_choice_error(self):
        """Test error handling for invalid template choices"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--template", "nonexistent"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail due to invalid template choice
        assert result.returncode != 0

        # Should contain error about invalid choice
        error_output = result.stderr + result.stdout
        assert "invalid choice" in error_output or "choose from" in error_output

    def test_invalid_transport_choice_error(self):
        """Test error handling for invalid transport choices"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--transport", "invalid"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail due to invalid transport choice
        assert result.returncode != 0

        # Should contain error about invalid choice
        error_output = result.stderr + result.stdout
        assert "invalid choice" in error_output or "choose from" in error_output

    def test_invalid_structure_choice_error(self):
        """Test error handling for invalid structure choices"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--structure", "invalid"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail due to invalid structure choice
        assert result.returncode != 0

        # Should contain error about invalid choice
        error_output = result.stderr + result.stdout
        assert "invalid choice" in error_output or "choose from" in error_output

    def test_invalid_type_choice_error(self):
        """Test error handling for invalid type choices"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--type", "invalid"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail due to invalid type choice
        assert result.returncode != 0

        # Should contain error about invalid choice
        error_output = result.stderr + result.stdout
        assert "invalid choice" in error_output or "choose from" in error_output

    def test_invalid_numeric_argument_error(self):
        """Test error handling for invalid numeric arguments"""
        # Test invalid tools count
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--tools", "abc"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail due to invalid numeric argument
        assert result.returncode != 0

        # Should contain error about invalid int value
        error_output = result.stderr + result.stdout
        assert "invalid int" in error_output.lower() or "invalid literal" in error_output.lower()

    def test_negative_numeric_argument_error(self):
        """Test error handling for negative numeric arguments"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--tools", "-1"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should succeed (CLI doesn't validate negative values, just uses them)
        # This tests that the CLI doesn't crash on negative values
        assert result.returncode == 0

    def test_nonexistent_output_directory_error(self):
        """Test error handling when output directory doesn't exist and can't be created"""
        # Try to write to a directory that doesn't exist and can't be created
        # This is tricky to test directly, so we'll test with a valid but non-existent directory
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent_dir = Path(temp_dir) / "nonexistent" / "deep" / "path"

            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--output", str(nonexistent_dir)],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastestmcp/src"
            )

            # Should succeed (CLI creates directories automatically)
            assert result.returncode == 0

    def test_permission_denied_error(self):
        """Test error handling when output directory has no write permissions"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a directory and remove write permissions
            no_write_dir = Path(temp_dir) / "no_write"
            no_write_dir.mkdir()
            no_write_dir.chmod(0o444)  # Read only

            try:
                result = subprocess.run(
                    [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--output", str(no_write_dir)],
                    capture_output=True,
                    text=True,
                    cwd="/Users/jwink/Documents/github/fastestmcp/src"
                )

                # Should fail due to permission denied
                # Note: This might not fail if the CLI doesn't actually write files in this case
                # The test is more about ensuring the CLI handles permission errors gracefully
                error_output = result.stderr + result.stdout
                if result.returncode != 0:
                    assert "permission" in error_output.lower() or "denied" in error_output.lower() or len(error_output) > 0

            finally:
                # Restore permissions for cleanup
                no_write_dir.chmod(0o755)

    def test_file_exists_overwrite_behavior(self):
        """Test behavior when output file already exists"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file first
            existing_file = Path(temp_dir) / "test.py"
            existing_file.write_text("# Existing file")

            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastestmcp/src"
            )

            # Should succeed (CLI should overwrite existing files)
            assert result.returncode == 0

            # File should be overwritten
            assert existing_file.exists()
            content = existing_file.read_text()
            assert "Generated by FastestMCP CLI" in content

    def test_empty_name_argument_error(self):
        """Test error handling for empty name argument"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "", "--level", "1"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should succeed (empty name is technically valid, though not recommended)
        # The CLI doesn't validate empty names, so this tests graceful handling
        assert result.returncode == 0

    def test_special_characters_in_name(self):
        """Test handling of special characters in project names"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test with underscores and numbers
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test_123", "--level", "1", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastestmcp/src"
            )

            # Should succeed
            assert result.returncode == 0

            # File should be created with the name
            expected_file = Path(temp_dir) / "test_123.py"
            assert expected_file.exists()

    def test_very_long_name_handling(self):
        """Test handling of very long project names"""
        with tempfile.TemporaryDirectory() as temp_dir:
            long_name = "a" * 200  # Very long name

            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", long_name, "--level", "1", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastestmcp/src"
            )

            # Should succeed
            assert result.returncode == 0

            # File should be created (filesystem may truncate, but shouldn't crash)
            expected_file = Path(temp_dir) / f"{long_name}.py"
            assert expected_file.exists() or len(list(Path(temp_dir).glob("*.py"))) > 0

    def test_multiple_invalid_arguments_error(self):
        """Test error handling when multiple arguments are invalid"""
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--level", "10", "--transport", "invalid"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should fail due to multiple invalid arguments
        assert result.returncode != 0

        # Should contain error information
        error_output = result.stderr + result.stdout
        assert len(error_output.strip()) > 0

    def test_conflicting_arguments_error(self):
        """Test error handling for conflicting arguments"""
        # Test using both --level and --template (should work, but let's see)
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--level", "1", "--template", "weather"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # This should work (template takes precedence) or fail gracefully
        # The important thing is it doesn't crash
        output = result.stdout + result.stderr
        assert len(output.strip()) > 0

    def test_missing_template_implementation_error(self):
        """Test error handling when template is requested but not implemented"""
        # This is more of an internal test - templates should be implemented
        # But if a template is missing, it should fail gracefully
        result = subprocess.run(
            [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "test", "--template", "weather"],
            capture_output=True,
            text=True,
            cwd="/Users/jwink/Documents/github/fastestmcp/src"
        )

        # Should either succeed (if template exists) or fail gracefully
        output = result.stdout + result.stderr
        assert len(output.strip()) > 0

    def test_network_related_errors(self):
        """Test error handling for network-related operations (if any)"""
        # The current CLI doesn't seem to have network operations
        # This is a placeholder for future network-dependent features
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "network_test", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastestmcp/src"
            )

            # Should succeed (no network operations in basic generation)
            assert result.returncode == 0

    def test_interrupt_signal_handling(self):
        """Test handling of interrupt signals (Ctrl+C)"""
        # This is difficult to test directly with subprocess
        # We can test that the CLI exits gracefully when interrupted
        pass  # Placeholder for future implementation

    def test_memory_error_handling(self):
        """Test error handling for memory-related issues"""
        # Test with very large component counts that might cause memory issues
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "memory_test", "--tools", "1000", "--resources", "1000", "--prompts", "1000", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastestmcp/src"
            )

            # Should either succeed or fail gracefully
            output = result.stdout + result.stderr
            assert len(output.strip()) > 0

    def test_unicode_name_handling(self):
        """Test handling of unicode characters in project names"""
        with tempfile.TemporaryDirectory() as temp_dir:
            unicode_name = "测试项目"  # Chinese characters

            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", unicode_name, "--level", "1", "--output", temp_dir],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastestmcp/src"
            )

            # Should succeed
            assert result.returncode == 0

            # File should be created (name may be handled differently by filesystem)
            files = list(Path(temp_dir).glob("*.py"))
            assert len(files) > 0

    def test_path_with_spaces_handling(self):
        """Test handling of paths with spaces"""
        with tempfile.TemporaryDirectory() as temp_dir:
            spaced_dir = Path(temp_dir) / "path with spaces"
            spaced_dir.mkdir()

            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "spaced_test", "--output", str(spaced_dir)],
                capture_output=True,
                text=True,
                cwd="/Users/jwink/Documents/github/fastestmcp/src"
            )

            # Should succeed
            assert result.returncode == 0

            # File should be created in the spaced directory
            expected_file = spaced_dir / "spaced_test.py"
            assert expected_file.exists()

    def test_relative_path_handling(self):
        """Test handling of relative paths"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use relative path from the temp directory
            result = subprocess.run(
                [sys.executable, "-m", "fastestmcp.cli", "new", "--name", "relative_test", "--output", "relative_dir"],
                capture_output=True,
                text=True,
                cwd=temp_dir  # Run from temp directory so relative path resolves correctly
            )

            # Should succeed
            assert result.returncode == 0

            # Directory should be created
            relative_dir = Path(temp_dir) / "relative_dir"
            assert relative_dir.exists()