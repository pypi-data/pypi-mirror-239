#!/usr/bin/env python
# coding: utf-8
import setuptools
from setuptools import setup

setup(
    name='robotgpt',
    version='0.0.2',
    author='blaze.zhang',
    author_email='blaze.zhang@cloudminds.com',
    url='https://src.cloudminds.com/ai-api/robotgptllm',
    description=u'RobotGPT LLM 支持Langchain',
    # packages=setuptools.find_packages(),
    install_requires=['langchain'],
)