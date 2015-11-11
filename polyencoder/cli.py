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
import argparse
import sys
from urllib import quote_plus
from .polyencoder import polyencode
try:
    from .polyencode_layer import encodelayer
except ImportError:
    encodelayer = None

DESC = """
    Encode coordinates with Google's encoded polyline algorithm
    see: https://developers.google.com/maps/documentation/utilities/polylinealgorithm
"""


def encodepoints(points):
    if len(points) == 1:
        in_points = sys.stdin.read().split(' ')
    else:
        in_points = points[1:]

    points = [(float(x), float(y)) for x, y in [point.split(',') for point in in_points]]

    points = polyencode(points)
    print(quote_plus(points))


def main():
    parser = argparse.ArgumentParser('polyencode', description=DESC)
    sp = parser.add_subparsers()

    points = sp.add_parser('points', usage='%(prog)s [points ...]', help="Encode a set of points")
    points.add_argument('points', nargs='*')
    points.set_defaults(func=encodepoints)

    if encodelayer:
        layer = sp.add_parser('layer', usage='%(prog)s [options] keys [infile]', help="Encode all features in a layer")

        layer.add_argument('keys', type=str, nargs='?', default='id', help='comma separated list of fields from file to include in CSV')
        layer.add_argument('infile', type=str)
        layer.add_argument('--no-encode', action='store_false', dest='encode', help="Don't urlencode the output string")
        layer.add_argument('--delimiter', type=str, default='\t', help="delimiter (default is tab)")
        layer.set_defaults(func=encodelayer)

    args = parser.parse_args()

    kwargs = vars(args)

    kwargs.pop('func')(**kwargs)

if __name__ == '__main__':
    main()
