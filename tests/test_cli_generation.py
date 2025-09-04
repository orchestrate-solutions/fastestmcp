import pytest
import tempfile
import os
import sys
import ast
from pathlib import Path

# Override TemporaryDirectory to use project-root/tmp_generated
class KeepTempDir(tempfile.TemporaryDirectory):
    def __enter__(self):
        project_root = Path(__file__).parent.parent
        dirpath = project_root / "tmp_generated"
        dirpath.mkdir(exist_ok=True)
        # Save for potential cleanup
        self.name = str(dirpath)
        return str(dirpath)

    def __exit__(self, exc_type, exc, tb):
        # If KEEP_GENERATED env var is set, do not cleanup
        if os.environ.get("KEEP_GENERATED"):
            return
        # Otherwise, remove generated directory
        import shutil
        shutil.rmtree(self.name, ignore_errors=True)

# Replace TemporaryDirectory globally
tempfile.TemporaryDirectory = KeepTempDir

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from fastestmcp.cli.template_handlers import generate_level_boilerplate
from fastestmcp.cli.main_generator import generate_complex_server
from fastestmcp.cli.template_handlers import generate_server_from_template


class TestCLIGeneration:
    """Test CLI code generation functionality"""

    def test_level_1_generation(self):
        """Test Level 1 boilerplate generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generate_level_boilerplate(1, "test_app", temp_dir)
            assert "Level 1 boilerplate generated" in result

            # Read the generated file
            generated_file = Path(temp_dir) / "test_app.py"
            assert generated_file.exists()

            with open(generated_file, 'r') as f:
                code = f.read()

            # Parse the generated code to ensure it's valid Python
            ast.parse(code)

            # Check that it contains expected components
            assert "from mcp.server.fastmcp import FastMCP" in code
            assert "register_tools" in code  # Changed from @app.tool decorator
            assert "register_component" in code  # New component system
            assert "count=1" in code  # Tool count parameter

            # Verify no old decorator patterns
            assert "add_tool" not in code  # Old pattern removed
            assert "tool_1" not in code  # Old pattern removed

    def test_level_2_generation(self):
        """Test Level 2 boilerplate generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generate_level_boilerplate(2, "test_app", temp_dir)
            assert "Level 2 boilerplate generated" in result

            generated_file = Path(temp_dir) / "test_app.py"
            assert generated_file.exists()

            with open(generated_file, 'r') as f:
                code = f.read()

            ast.parse(code)
            assert "from mcp.server.fastmcp import FastMCP" in code
            assert "register_tools" in code  # Changed from @app.tool decorator
            assert "register_resources" in code  # Changed from @app.resource decorator
            assert "register_component" in code  # New component system

            # Verify tool and resource counts in registration calls
            assert "count=2" in code  # Should have 2 tools
            assert "count=1" in code  # Should have 1 resource

            # Verify no old decorator patterns
            assert "add_tool" not in code  # Old pattern removed
            assert "add_resource" not in code  # Old pattern removed

    def test_invalid_level_raises_error(self):
        """Test that invalid level raises ValueError"""
        with pytest.raises(ValueError, match="Invalid level: 99"):
            generate_level_boilerplate(99, "test_app", ".")

    def test_generated_code_syntax_validity(self):
        """Test that all generated levels produce syntactically valid Python"""
        with tempfile.TemporaryDirectory() as temp_dir:
            for level in range(1, 6):
                result = generate_level_boilerplate(level, f"test_level_{level}", temp_dir)
                assert f"Level {level} boilerplate generated" in result
                
                if level <= 2:
                    # Levels 1-2 generate single files
                    generated_file = Path(temp_dir) / f"test_level_{level}.py"
                    assert generated_file.exists()
                    
                    with open(generated_file, 'r') as f:
                        code = f.read()
                    
                    # This will raise SyntaxError if code is invalid
                    ast.parse(code)
                else:
                    # Levels 3-5 generate structured directories
                    generated_dir = Path(temp_dir) / f"test_level_{level}"
                    assert generated_dir.exists()
                    assert generated_dir.is_dir()
                    
                    # Check that main Python files exist and are syntactically valid
                    python_files = list(generated_dir.glob("*.py")) + list(generated_dir.glob("app/*.py"))
                    assert len(python_files) > 0, f"No Python files found for level {level}"
                    
                    for py_file in python_files:
                        with open(py_file, 'r') as f:
                            code = f.read()
                        
                        # This will raise SyntaxError if code is invalid
                        ast.parse(code)

    def test_complex_server_generation(self):
        """Test complex server generation with custom parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result, folder_structure = generate_complex_server(
                "test_complex", 3, 2, 1, 0, 0, "stdio", "mono", "fastmcp", temp_dir
            )

            # Check that files were created
            server_file = Path(temp_dir) / "test_complex.py"
            assert server_file.exists()

            # Check file content
            content = server_file.read_text()
            assert "test_complex" in content

            # Verify component-based registration (new MCP-compliant approach)
            assert "register_component" in content
            assert "register_tools" in content
            assert "register_resources" in content
            assert "register_prompts" in content

            # Verify tool count in registration call
            assert 'count=3' in content  # Should register 3 tools
            assert 'count=2' in content  # Should register 2 resources
            assert 'count=1' in content  # Should register 1 prompt

            # Verify FastMCP usage
            assert "FastMCP" in content
            assert "app = FastMCP" in content

            # Verify no old decorator patterns
            assert "add_tool" not in content  # Old pattern removed
            assert "add_resource" not in content  # Old pattern removed

    def test_server_generation_with_notifications(self):
        """Test server generation with notification and subscription parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result, folder_structure = generate_complex_server(
                "test_notifications", 2, 1, 0, 3, 2, "stdio", "mono", "fastmcp", temp_dir
            )

            # Check that files were created
            server_file = Path(temp_dir) / "test_notifications.py"
            assert server_file.exists()

            # Check file content for MCP-compliant server code
            content = server_file.read_text()
            assert "test_notifications" in content

            # Verify component-based registration (new MCP-compliant approach)
            assert "register_component" in content
            assert "register_tools" in content
            assert "register_resources" in content
            assert "register_notifications" in content
            assert "register_subscriptions" in content

            # Verify FastMCP usage
            assert "FastMCP" in content
            assert "app = FastMCP" in content

            # Verify no old decorator patterns
            assert "@server.subscription" not in content  # Old pattern removed
            assert "@app.tool" not in content  # Old pattern removed
            # Note: "notification_" may appear in comments/function names in the new component system

    def test_client_generation_with_notifications(self):
        """Test client generation with notification and subscription parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            from fastestmcp.cli.client_generator import generate_complex_client
            result, folder_structure = generate_complex_client(
                "test_client_notifications", 2, 1, 1, 2, 1, "stdio", "mono", "fastmcp", temp_dir
            )

            # Check that files were created
            client_file = Path(temp_dir) / "test_client_notifications_client.py"
            assert client_file.exists()

            # Check file content for MCP-compliant client code
            content = client_file.read_text()
            assert "test_client_notifications" in content
            assert "Test_Client_NotificationsClient" in content

            # Verify MCP primitives are present (new MCP-compliant approach)
            assert "list_tools" in content
            assert "call_tool" in content
            assert "list_resources" in content
            assert "read_resource" in content
            assert "list_prompts" in content
            assert "render_prompt" in content
            assert "send_log" in content
            assert "request_elicitation" in content
            assert "request_sampling" in content

            # Verify connection management
            assert "connect" in content
            assert "disconnect" in content
            assert "_connected" in content

            # Verify MCP compliance - no old non-MCP concepts
            assert "add_notification" not in content  # Old pattern removed
            assert "get_notifications" not in content  # Old pattern removed
            assert "subscribe" not in content  # Old pattern removed
            assert "unsubscribe" not in content  # Old pattern removed
            assert "PRIORITY_MAP" not in content  # Old pattern removed
            assert "heapq" not in content  # Old pattern removed

    def test_template_generation(self):
        """Test template-based generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            generate_server_from_template("weather", "weather_app", temp_dir)

            # Check that file was created
            server_file = Path(temp_dir) / "weather_app.py"
            assert server_file.exists()

            content = server_file.read_text()
            assert "weather" in content.lower()
            assert "register_tools" in content  # Changed from @app.tool
