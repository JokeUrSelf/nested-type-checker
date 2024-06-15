from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="nested_type_checker",
    version="0.9.7",
    description="A runtime strict type-checking module for Python designed to validate parametrized (nested) types.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="JokeUrSelf",
    license="MIT",
    url="https://github.com/JokeUrSelf/nested-type-checker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    platforms=["any"],
)
