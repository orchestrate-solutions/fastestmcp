"""
Server generation functions for FastestMCP CLI
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Import templates and utilities
from .templates import TEMPLATES
from .generators import generate_tools_file, generate_resources_file, generate_prompts_file
from .utils import (
    generate_pyproject_toml,
    generate_main_py,
    generate_http_server_file,
    generate_stdio_server_file,
    generate_modular_app_components,
    generate_server_folder_markdown
)

# Import specialized modules
from .mono_server_generator import generate_mono_server_file
from .structured_server_generator import generate_main_server, generate_additional_files
from .file_generators import generate_readme, generate_folder_markdown
from .template_handlers import generate_level_boilerplate, generate_server_from_template
from .main_generator import generate_complex_server


# Main generation function is imported from main_generator module