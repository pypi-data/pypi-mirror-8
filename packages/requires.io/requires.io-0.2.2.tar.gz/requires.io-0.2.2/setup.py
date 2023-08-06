# -*- coding: utf-8 -*-
import os

# allow setup.py to be run from any path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    import setuptools
except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
from setuptools import setup

install_requires = ['requests >= 2.0.0', ]

try:
    import argparse
except ImportError:
    install_requires.append('argparse >= 1.2.0')

setup(
    name='requires.io',
    version='0.2.2',
    description='requires.io API',
    long_description=str(open('README.rst', 'rb').read()),
    url='https://requires.io/',
    author='Shining Panda S.A.S.',
    author_email='support@requires.io',
    packages=['requires_io', ],
    include_package_data=False,
    zip_safe=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'requires.io = requires_io.commands:main',
        ],
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
)

