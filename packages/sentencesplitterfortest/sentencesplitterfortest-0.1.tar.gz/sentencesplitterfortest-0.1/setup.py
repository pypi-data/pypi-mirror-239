from setuptools import setup, find_packages

setup(
    name="sentencesplitterfortest",
    version="0.1",
    author="Junyi Ye",
    description="A Python library to split text into sentences.",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0",
        # Add other dependencies if needed
    ],
)
