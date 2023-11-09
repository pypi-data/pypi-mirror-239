from setuptools import setup, find_packages
from pathlib import Path

version = (Path(__file__).parent / 'VERSION.txt').read_text().strip()

setup(
    name="sigmoidpythonpackage",
    version=version,
    packages=find_packages(),
    install_requires=["pandas"]
)