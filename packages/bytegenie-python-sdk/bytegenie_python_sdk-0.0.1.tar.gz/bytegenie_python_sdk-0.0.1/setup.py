"""
Setup file
"""

from setuptools import setup, find_packages

setup(
    name="bytegenie_python_sdk",
    version="0.0.1",
    author="ByteGenie",
    packages=find_packages(),
    install_requires=[
        'pandas', 'requests', 'numpy'
    ],
)
