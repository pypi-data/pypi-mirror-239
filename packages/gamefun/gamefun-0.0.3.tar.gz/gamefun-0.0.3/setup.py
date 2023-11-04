# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.0.3'

setup(
    name='gamefun',  # package name
    version=VERSION,  # package version
    author='Lei Cui',
    author_email='cuilei798@qq.com',
    maintainer='Lei Cui',
    maintainer_email='cuilei798@qq.com',
    license='MIT License',
    platforms=["linux"],

    description='Game package',
    long_description=open('README.md').read(),
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'pygame',
        # Add more dependencies here
    ],
    package_data={
        'Utils': ['Utils/*']
    },
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3',
)
