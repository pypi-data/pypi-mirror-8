#!/usr/bin/env python
from setuptools import setup, find_packages

__version__ = "0.1"


setup(
    name="flowzillow",
    author="Gregory Rehm",
    version=__version__,
    description="An intuitive python wrapper around the Zillow API",
    packages=find_packages(),
    package_data={"*": ["*.html"]},
    install_requires=[
        "requests"
    ],
)
