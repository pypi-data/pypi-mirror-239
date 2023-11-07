#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autosubmitconfigparser",
    version="1.0.50",
    author="Daniel Beltran Mora",
    author_email="daniel.beltran@bsc.es",
    description="An utility library that allows to read an Autosubmit 4 experiment configuration.",
    keywords=['climate', 'weather', 'workflow', 'HPC'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://earth.bsc.es/gitlab/ces/autosubmit4-config-parser.git",
    include_package_data=True,
    package_data={'files': ['autosubmitconfigparser/conf/files/*']},
    packages=setuptools.find_packages(),
    install_requires=['cython','ruamel.yaml==0.17.21','packaging>19', 'six>=1.10.0', 'configobj>=5.0.6', 'argparse>=1.4.0', 'python-dateutil>=2.8.2',
                       'pyparsing>=3.0.7', 'mock>=4.0.3', 'portalocker>=2.3.2', 'networkx>=2.6.3', 'requests>=2.27.1',
                      'bscearth.utils>=0.5.2', 'cryptography>=36.0.1', 'setuptools>=60.8.2',
                      'pip>=22.0.3', 'pythondialog', 'pytest', 'nose', 'coverage', 'PyNaCl>=1.4.0',
                      'Pygments'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux"
    ],
)
