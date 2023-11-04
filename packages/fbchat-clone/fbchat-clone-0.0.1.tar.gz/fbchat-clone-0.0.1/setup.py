import os
from setuptools import setup, find_packages

PATH = os.path.abspath(os.path.dirname(__file__))
VERSION = '0.0.1'
DESCRIPTION = 'Clone from fbchat'

setup(
    name="fbchat-clone",
    version=VERSION,
    author="fbchat",
    author_email="<fbchat@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'fbchat'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: PostgreSQL License",
        "Operating System :: MacOS :: MacOS X",
    ]
)
