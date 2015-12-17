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
Encode coordinates with Google's encoded polyline algorithm.
see: https://developers.google.com/maps/documentation/utilities/polylinealgorithm
"""
LAYER_DESC = """
Encode a set of points

positional arguments:
  [x,y x,y ...]  List of lon,lat coordinates
"""

def encodepoints(points, encode=True):
    split_points = (p.split(',') for p in points)
    poly = polyencode([(float(x), float(y)) for x, y in split_points])

    if encode:
        poly = quote_plus(poly)

    print(poly, file=sys.stdout)


def main():
    fc = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser('polyencode', description=DESC, formatter_class=fc)

    sp = parser.add_subparsers()

    points = sp.add_parser('points', usage='%(prog)s [x,y x,y ...]', description=LAYER_DESC, formatter_class=fc)
    points.add_argument('--no-encode', action='store_false', dest='encode', help='Disable url-encoding')
    points.set_defaults(func=encodepoints)

    if encodelayer:
        layer = sp.add_parser('layer', usage='%(prog)s [options] keys [infile]', description="Encode all features in a layer")
        layer.add_argument('keys', type=str, nargs='?', default='id', help='comma separated list of fields from file to include in CSV')
        layer.add_argument('infile', type=str, default='-')
        layer.add_argument('--delimiter', type=str, default='\t', help="delimiter (default is tab)")
        layer.add_argument('--no-encode', action='store_false', dest='encode', help='Disable url-encoding')
        layer.set_defaults(func=encodelayer)

    args, points = parser.parse_known_args()

    if args.func == encodepoints:
        if len(points) == 0:
            args.points = sys.stdin.read().strip().split(' ')
        else:
            args.points = points

    elif args.func == encodelayer:
        if args.infile in ('-', '/dev/stdin'):
            args.infile = sys.stdin

    kwargs = vars(args)
    kwargs.pop('func')(**kwargs)

if __name__ == '__main__':
    main()
