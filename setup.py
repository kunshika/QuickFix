from setuptools import setup, find_packages

setup(
    name="QuickFix",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich",
        "google-generativeai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "qfix=qfix.main:main",
        ],
    },
    author="Code Formatter Tool",
    description="A CLI tool to format and explain code using AI",
    python_requires=">=3.8",
)
