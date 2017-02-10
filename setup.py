#!/usr/bin/python2
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
import rouge_align
setup(
 
    name='rouge_align',
    version=rouge_align.__version__,
    packages=find_packages(),
    author="pltrdy",
    author_email="pltrdy@gmail.com",
    description="Text alignment using ROUGE score￼Edit",
    long_description=open('README.md').read(),
 
    # Ex: ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
    # install_requires= ,
 
 
    url='https://github.com/pltrdy/rouge_align',
    classifiers=[
        "Programming Language :: Python",
    ],
    entry_points = {
        'console_scripts': [
            'rouge_align = rouge_align.align:cmd',
        ],
    },
    license="MIT",
 
)
