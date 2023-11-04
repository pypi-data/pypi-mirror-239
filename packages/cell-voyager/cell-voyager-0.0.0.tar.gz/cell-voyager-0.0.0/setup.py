
import setuptools
import re
import os
import sys


setuptools.setup(
    name="cell-voyager",
    version="0.0.0",
    python_requires=">3.9.0",
    author="Michael E. Vinyard",
    author_email="mvinyard.ai@gmail.com",
    url=None,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="Voyager for cell data.",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
