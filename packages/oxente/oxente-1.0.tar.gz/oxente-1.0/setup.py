#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

try:
    long_description = file('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='oxente',
    version='1.0',
    url='https://github.com/luanfonceca/oxente',
    license='MIT',
    description=u'Tradução do módulo "this" do python para PT-BR-NE (Português brasileiro nordestino)',
    long_description=long_description,
    author='Luan Fonseca',
    author_email='luanfonceca@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=['oxente'],
    install_requires=['setuptools'],
)
