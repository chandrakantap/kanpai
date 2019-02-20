from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kanpai",
    version="0.1.9",
    keywords="schema json validation request-validation input-validation",
    author="Chandrakanta Pal",
    author_email="pal.chandrakanta@gmail.com",
    description="Python JSON schema validator with better error message",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/chandrakantap/kanpai.git",
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
