"""Setup script for World Model"""

from setuptools import setup, find_packages

setup(
    name="world-model",
    version="0.1.0",
    description="Local Consciousness Knowledge System for Esoterica",
    author="Human-AI Collaboration",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "networkx>=3.0",
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0",
        "pyyaml>=6.0",
        "markdown>=3.4",
        "beautifulsoup4>=4.12",
        "python-frontmatter>=1.0.0",
        "click>=8.1",
        "rich>=13.0",
    ],
    extras_require={
        "api": [
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
            "websockets>=11.0",
        ],
        "llm": [
            "anthropic>=0.18.0",
            "ollama>=0.1.0",
        ],
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "world-model=cli:main",
        ],
    },
)
