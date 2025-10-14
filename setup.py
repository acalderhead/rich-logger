from setuptools import setup, find_packages

setup(
    name="rich_logger",
    version="0.1.0",
    description="Custom Rich-enhanced logger with semantic logging methods.",
    author="Aidan Calderhead",
    author_email="aidan.calderhead@gmail.com",
    url="https://github.com/acalderhead/rich-logger",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "rich>=13.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
