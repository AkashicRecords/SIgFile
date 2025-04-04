from setuptools import setup, find_packages

setup(
    name="sigfile-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "sigfile=sigfile_cli.cli:main",
        ],
    },
    author="Sam Elder",
    author_email="samelder@example.com",
    description="Command Line Interface for SigFile - Developer Signature Tracking",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sigfile-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
) 