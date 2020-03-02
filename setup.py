from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kanpai",
    use_scm_version=True,
    keywords="schema json validation request-validation input-validation",
    author="Chandrakanta Pal",
    author_email="pal.chandrakanta@gmail.com",
    description="Python JSON schema validator with better error message",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/chandrakantap/kanpai",
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
