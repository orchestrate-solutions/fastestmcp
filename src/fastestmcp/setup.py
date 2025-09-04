from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastestmcp",
    version="1.0.2",
    author="Orchestrate LLC",
    author_email="hello@orchestrate.solutions",
    description="Super Simple MCP Server Development - Zero-config, one-command creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orchestrate-solutions/fastestmcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
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
