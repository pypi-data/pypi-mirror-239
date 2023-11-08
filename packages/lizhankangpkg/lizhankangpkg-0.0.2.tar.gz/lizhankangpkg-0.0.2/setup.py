# coding:utf-8 
# @Author : lizhankang
# @Subject : 
# @Time : 2023 - 11 - 08
from setuptools import setup

setup(
    name='lizhankangpkg',
    version='0.0.2',
    install_requires=[
        'requests',
        'importlib-metadata; python_version > "3.6"',
    ],
)