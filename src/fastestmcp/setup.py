from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastestmcp",
    version="0.1.0",
    author="FastestMCP Team",
    author_email="fastestmcp@example.com",
    description="Super Simple MCP Server Development - Zero-config, one-command creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoshuaWink/fastmcp-templates",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastmcp>=0.9.0",
        "requests",  # For web scraping component
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black",
            "flake8",
        ],
        "web": [
            "beautifulsoup4",  # For advanced web scraping
            "selenium",  # For JavaScript-heavy sites
        ],
        "database": [
            "sqlalchemy",
            "alembic",
        ],
        "ai": [
            "openai",  # For AI-assisted development
            "anthropic",  # Alternative AI provider
        ],
    },
    entry_points={
        "console_scripts": [
            "fastestmcp=fastestmcp.cli:main",
        ],
    },
)