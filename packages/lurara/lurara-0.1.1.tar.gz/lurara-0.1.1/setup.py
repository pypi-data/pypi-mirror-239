#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
    name='lurara',
    version='0.1.1',
    description='more easy use for keras(care for it used in small or mid model, not efficiency). simplify like dataset create, model train&predict. Used by person',
    author_email='2229066748@qq.com',
    maintainer="Eagle'sBaby",
    maintainer_email='2229066748@qq.com',
    packages=find_packages(),
    license='Apache Licence 2.0',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords = ['keras', 'utils'],
    python_requires='>=3',
    install_requires=[
        "tensorflow-gpu==2.6.0",
        "keras==2.6.0",
        "files3"
    ],
)

