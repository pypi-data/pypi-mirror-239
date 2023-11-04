#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import configparser
import os

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = [
    "abbreviations",
    "beautifulsoup4",
    "braceexpand",
    "coloredlogs",
    "ConfigArgParse",
    "lxml",
    "nltk",
    "pandas",
    "pygetpapers",
    "pytest",
    "setuptools",
    "spacy",
    "tkinterweb",
    "tqdm",
]

setup(
    name="docanalysis",
    version="0.2.8",
    description="extract structured information from ethics paragraphs",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Ayush Garg, Shweata N. Hegde",
    author_email="ayush@science.org.in, shweata.hegde@gmail.com",
    url="https://github.com/petermr/docanalysis",
    packages=[
        "docanalysis",
    ],
    package_dir={"docanalysis": "docanalysis"},
    include_package_data=True,
    install_requires=requirements,
    license="Apache License",
    zip_safe=False,
    keywords="research automation",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "docanalysis=docanalysis.docanalysis:main",
        ],
    },
)
