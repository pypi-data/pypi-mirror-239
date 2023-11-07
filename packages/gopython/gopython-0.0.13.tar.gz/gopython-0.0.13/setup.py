from setuptools import setup, find_packages
import codecs
import os
import requests
import flask

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = 'Flask Library for set ACL in Flsk app.'


# Setting up
setup(
    name="gopython",
    version=VERSION,
    author="Ashok Mamnani",
    author_email="ashok.mamnani@ascentinfo.solutions",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["requests", "flask"],
    keywords=['python', 'go'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)