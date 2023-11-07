#!python

import setuptools
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('PiecewiseBeta/PiecewiseBeta.py').read(),
    re.M).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name="PiecewiseBeta",
    version=version,
    author="David Blair",
    author_email="david.blair@ucsf.edu",
    description="A small class that carries out computations for the Piecewise Beta Distribution.",
    long_description_content_type="text/markdown",
    url="https://github.com/daverblair/PiecewiseBeta",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
