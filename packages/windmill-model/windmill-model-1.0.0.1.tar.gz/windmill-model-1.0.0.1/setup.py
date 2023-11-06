# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/11 18:53
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : setup.py
# @Software: PyCharm
"""
import os

from setuptools import setup, find_packages

VERSION = '1.0.0.1'


def _parse_requirements(fname):
    with open(fname, encoding="utf-8-sig") as f:
        requirements = f.readlines()
    return requirements


setup(
    name='windmill-model',
    version=VERSION,
    description="sdk in python for windmill model",
    install_requires=_parse_requirements('./requirements.txt'),
    packages=find_packages(exclude=()),
    url='https://console.cloud.baidu-int.com/devops/icode/repos/baidu/themis/windmill-model/tree/master',
    python_requires='>=3.6',
)