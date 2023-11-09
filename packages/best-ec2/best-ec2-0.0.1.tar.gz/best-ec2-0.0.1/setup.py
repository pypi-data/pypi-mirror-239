#!/usr/bin/env python3
import setuptools

setuptools.setup(
    python_requires=">3.8.0",
    install_requires=[
        'boto3 >=1.23.10',
        'lambda-thread-pool >=0.0.2',
    ]
)