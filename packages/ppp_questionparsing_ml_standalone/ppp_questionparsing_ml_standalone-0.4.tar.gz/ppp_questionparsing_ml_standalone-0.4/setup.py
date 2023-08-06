#!/usr/bin/env python3
import os
import glob
from setuptools import setup, find_packages



setup(
    name='ppp_questionparsing_ml_standalone',
    version='0.4',
    description='Compute triplets from a question, with an ML approach',
    url='https://github.com/ProjetPP',
    author='Quentin Cormier',
    author_email='quentin.cormier@ens-lyon.fr',
    license='MIT',
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Development Status :: 1 - Planning',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'ppp_datamodel>=0.5',
        'ppp_libmodule>=0.7',
        'nltk',
        'numpy'
    ],
    packages=[
        'ppp_questionparsing_ml_standalone',
    ],
    package_data={'ppp_questionparsing_ml_standalone': ['data/*']},

)

import sys
if 'install' in sys.argv:
    import nltk
    nltk.download("punkt")
