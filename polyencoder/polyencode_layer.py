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

from __future__ import print_function
import sys
import csv
from urllib import quote_plus
import fiona
from .polyencoder import polyencode


def getproperties(feature, keys):
    '''Return a list of properties from feature'''
    return [feature['properties'].get(k) for k in keys]


def encodelayer(infile, keys, encode=None, delimiter=None):
    keys = keys.split(',')

    writer = csv.writer(sys.stdout, delimiter=delimiter or '\t')

    with fiona.drivers():
        with fiona.open(infile, 'r') as layer:

            for feature in layer:
                if feature['geometry']['type'] == 'MultiPolygon':
                    # list of list of lists of tuples
                    coords = feature['geometry']['coordinates'][0][0]

                elif feature['geometry']['type'] == 'Polygon' or feature['geometry']['type'] == 'MultiLineString':
                    # list of lists of tuples
                    coords = feature['geometry']['coordinates'][0]

                elif feature['geometry']['type'] == 'Linestring':
                    # list of tuples
                    coords = feature['geometry']['coordinates']

                else:
                    raise NotImplementedError(
                        "Polyencode not available for geometry type: {}".format(feature['geometry']['type']))
                try:
                    encoded = polyencode(coords)

                except TypeError:
                    print("Unexpected issue with {}".format(feature['properties'].get(keys[0])), file=sys.stderr)
                    raise

                if encode:
                    encoded = quote_plus(encoded)

                props = getproperties(feature, keys) + [encoded]
                writer.writerow(props)
