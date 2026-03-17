from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-paperclip",
    version="1.0.0",
    description="CLI harness for the Paperclip agent orchestration platform",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    install_requires=[
        "click>=8.0.0",
        "prompt-toolkit>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cli-anything-paperclip=cli_anything.paperclip.paperclip_cli:main",
        ],
    },
    python_requires=">=3.10",
)
