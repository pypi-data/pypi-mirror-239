# -*- coding: utf-8 -*-
# @File    : setup.py.py
# @Create_Time    : 2023-11-07 9:49
# @Author  : cwc
# @Description : 
import setuptools

setuptools.setup(
    name='scriptmodule',
    version='0.0.1',
    author='cwc',
    author_email='idonotknow@idonotknow.com',
    description='i donot know too',
    long_description_content_type='text/markdown',  # 长文描述的文本格式
    url='https://pypi.org/',  # 项目主页
    packages=setuptools.find_packages(),
    classifiers=[  # 包的分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
