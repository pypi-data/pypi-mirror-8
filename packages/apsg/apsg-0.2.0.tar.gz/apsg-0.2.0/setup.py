#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'numpy >= 1.8',
    'matplotlib >= 1.2'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='apsg',
    version='0.2.0',
    description='APSG - structural geology module for Python',
    long_description=readme + '\n\n' + history,
    author='Ondrej Lexa',
    author_email='lexa.ondrej@gmail.com',
    url='http://ondrolexa.github.io/apsg',
    packages=[
        'apsg',
    ],
    package_dir={'apsg':
                 'apsg'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='apsg',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
