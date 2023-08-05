#!/usr/bin/env python
#
# -*- mode:python; sh-basic-offset:4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim:set tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8:
#

import os
import pip.req
import setuptools
import sys

import clustoapi


reqs = 'requirements.txt'

for arg in sys.argv[1:]:
    if arg == 'test':
        reqs = 'test-requirements.txt'
    if arg == 'develop':
        reqs = 'dev-requirements.txt'

readme = os.path.join(os.path.dirname(sys.argv[0]), 'README.rst')
reqs = os.path.join(os.path.dirname(sys.argv[0]), reqs)

install_requires = pip.req.parse_requirements(reqs)
dependency_links = set([str(_.url) for _ in install_requires if _.url])
install_requires = set([str(_.req) for _ in install_requires])

# These two were introduced in 2.7
if sys.version_info < (2, 7):
    install_requires.extend([
        'importlib',
        'argparse'
    ])


setuptools.setup(
    name='clusto-apiserver',
    url='https://github.com/clusto/clusto-apiserver',
    version=clustoapi.__version__,
    packages=setuptools.find_packages(),
    author=clustoapi.__authors__[0][1],
    author_email=clustoapi.__authors__[0][0],
    description=clustoapi.__desc__,
    long_description=open(readme).read(),
    license='BSD',
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': [
            'clusto-apiserver=clustoapi.server:main'
        ],
    },
    zip_safe=False,
    test_suite='tests.all.test_suites',
)
