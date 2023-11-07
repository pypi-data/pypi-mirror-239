#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setup.py
@Describe :  
@Contact :   mrbingzhao@qq.com
@License :   (C)Copyright 2023/11/7, Liugroup-NLPR-CASIA

@Modify Time        @Author       @Version    @Desciption
----------------   -----------   ---------    -----------
2023/11/7 下午1:55   liubingzhao      1.0           ml
'''
from setuptools import setup, find_packages

setup(
    name='bzutil',
    version='1.0.1',
    author='mrbingzhao',
    author_email='mrbingzhao@qq.com',
    description='Integrates a number of commonly used Python functions, methods, algorithms, and other toolkits for easy reuse.',
    packages=find_packages(exclude=["*.tests"]),
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
)