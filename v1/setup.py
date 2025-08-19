from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="document-reader",
    version="1.0.0",
    author="Document Reader Team",
    author_email="example@example.com",
    description="A flexible API for processing documents using various technologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/document-reader",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "document-reader=app.main:start",
        ],
    },
)