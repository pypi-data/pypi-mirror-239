'''
FilePath: setup.py
Author: yongze.chen
Date: 2023-11-05 20:32:59 +0800
LastEditors: yongze.chen~home yongze@dingtalk.com
Email: yongze@dingtalk.com
LastEditTime: 2023-11-05 21:21:16 +0800
Copyright: 2023 Yong CO.,LTD. All Rights Reserved.
Descripttion: 
'''
#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='yong_wechat',
    version='23.11.6',
    author='yongze',
    author_email='yongze@dingtalk.com',
    url='https://github.com/chenyongze',
    license='MIT',
    keywords=['yong', 'utils'],
    long_description='https://github.com/chenyongze',
    description=u'yong_wechat',
    packages=['yong_wechat'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jujube=yong_wechat:jujube',
            'pill=yong_wechat:pill'
        ]
    }
)