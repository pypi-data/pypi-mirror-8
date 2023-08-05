#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


with open('README.rst') as file:
    long_description = file.read()

setup(
    name='MongoNotebookManager',
    version='1.0.0',
    description='A notebook manager for IPython with MongoDB as the backend.',
    long_description=long_description,
    author='Laurence Putra',
    author_email='laurenceputra@gmail.com',
    url = 'https://github.com/laurenceputra/mongo_notebook_manager',
    license = 'GPL v3',
    packages = ['mongo_notebook_manager'],
    package_dir = {'mongo_notebook_manager': 'mongo_notebook_manager'},
    keywords = 'mongo notebook manager ipython database storage',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Database :: Front-Ends',
        'Framework :: IPython',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'pymongo',
        'ipython<3'
    ],
    entry_points={
        'console_scripts': [
            'notebooks_importer = mongo_notebook_manager.notebooks_importer:main'
        ]
    },
)
