#!/usr/bin/env python
# -*- coding: utf-8 -*-

# polyencoder
# Copyright 2015 Neil Freeman contact@fakeisthenewreal.org

# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from setuptools import setup

try:
    README = open('README.rst').read()
except IOError:
    README = ''

setup(
    name='polyencoder',
    version='0.1.1',
    description='Encode geometries and geo layers with the GPolyencoder algorithm',
    long_description=README,
    keywords='polygons gis mapping',
    author='fitnr',
    license='BSD',
    author_email='contact@fakeisthenewreal.org',
    packages=['polyencoder'],

    url='https://github.com/fitnr/polyencoder',

    include_package_data=False,

    extras_require={
        'layer': ['Fiona']
    },

    zip_safe=True,

    use_2to3=True,

    test_suite='tests',

    entry_points={
        'console_scripts': [
            'polyencode=polyencoder.cli:main',
        ],
    },
)
