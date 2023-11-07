
# -- import packages: ----------------------------------------------------------
import setuptools
import re
import os
import sys


# -- run setup: ----------------------------------------------------------------

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="torch-nets",
    version="0.1.0",
    python_requires=">3.9.0",
    author="Michael E. Vinyard",
    author_email="mvinyard.ai@gmail.com",
    url=None,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="API to compose PyTorch neural networks on the fly.",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
