from setuptools import setup, find_packages

# Read the dependencies from pyproject.toml or use minimal defaults
install_requires = [
    "fastmcp>=2.12.0",
    "httpx>=0.28.0",
]

setup(
    name="fastestmcp",
    version="1.0.2",
    description="Generate production-ready MCP servers and clients in seconds with the FastestMCP CLI",
    author="Orchestrate LLC",
    author_email="hello@orchestrate.solutions",
    url="https://github.com/orchestrate-solutions/fastestmcp",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_requires,
    python_requires=">=3.10",
    entry_points={
        'console_scripts': [
            'fastestmcp=fastestmcp.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)