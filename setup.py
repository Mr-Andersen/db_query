#!/usr/bin/env python3

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='db_query',
    version='1.1.1',
    author='Andrew Anderson',
    author_email='andrew-anderson.neo@yandex.ru',
    description='Module for comfortable using of database '
                '(tested for sqlite3)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Mr-Andersen/db_query',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[]
)
