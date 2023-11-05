"""
Setup file
"""

from setuptools import setup, find_packages

setup(
    name="bytegenie-python-sdk",
    version="0.0.0",
    author="ByteGenie",
    packages=find_packages(),
    install_requires=[
        'pandas', 'requests', 'numpy'
    ],
)
