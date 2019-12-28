#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LizardDLCAnalysis Toolbox
© Jojo S.
Licensed under MIT License
"""

import setuptools

setuptools.setup(
    name='lizardanalysis',
    version='0.1',
    author='Jojo Schultz',
    #py_modules=['lizardanalysis'],
    install_requires=[
        'Click', 'ipython', 'numpy', 'scipy', 'pandas', 'matplotlib', 'os', 'glob', 'ruamel.yaml', 'tkinter',
        'tkFileDialog'
    ],
    packages=setuptools.find_packages(),
    data_files=[('lizardanalysis',['lizardanalysis/config.yaml'])],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        lizardanalysis=lizardanalysis:main
    ''',
)