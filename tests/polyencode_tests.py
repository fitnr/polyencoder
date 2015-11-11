#!/usr/bin/env python

# Copyright (c) 2009, Koordinates Limited
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

#   * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#   * Neither the name of the Koordinates Limited nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import re
import unittest
import json
from polyencoder import polyencoder


class PolyEncoderTest(unittest.TestCase):

    def setUp(self):
        self.e = polyencoder.PolyEncoder()

    def test_glineenc(self):
        # use same tests & setup as glineenc
        e = polyencoder.PolyEncoder(num_levels=4, zoom_factor=32, threshold=0.00001)

        p = ((-120.2, 38.5), (-126.453, 43.252), (-120.95, 40.7))
        r = e.polyencode(p)
        self.assertEqual(r, '_p~iF~ps|U_c_\\fhde@~lqNwxq`@')

        p = ((-122.1419, 37.4419), (-122.1519, 37.4519), (-122.1819, 37.4619),)
        r = e.polyencode(p)
        self.assertEqual(r, 'yzocFzynhVq}@n}@o}@nzD')

        p = [(-120.2, 38.5)]
        r = e.polyencode(p)
        self.assertEqual(r, '_p~iF~ps|U')

    def test_java(self):
        # use same tests & setup as Java
        e = polyencoder.PolyEncoder(18, 2, 0.00001, True)
        p = ((8.94328, 52.29834), (8.93614, 52.29767), (8.93301, 52.29322), (8.93036, 52.28938), (8.97475, 52.27014))
        r = e.polyencode(p)
        # JS:                         "soe~Hovqu@dCrk@xZpR~VpOfwBmtG",          "PG@IP"
        # Java:                       'soe~Hovqu@dCrk@xZpR~VpOfwBmtG',          'PPPPP'
        self.assertEqual(r, 'soe~Hovqu@dCrk@xZpR~VpOfwBmtG')

    def test_googleutility(self):
        expected = '}vq~FlwcvOheAuoH'
        p = ((-87.67879, 41.87519), (-87.63004, 41.86394))
        result = polyencoder.PolyEncoder(num_levels=3).polyencode(p)

        self.assertEqual(result, expected)

    def test_glineenc_encode_number(self):
        # use same tests & setup as glineenc
        self.assertEqual(polyencoder.encode_signed_number(int(-179.9832104 * 1E5)), '`~oia@')
        self.assertEqual(polyencoder.encode_signed_number(int(-120.2 * 1E5)), '~ps|U')
        self.assertEqual(polyencoder.encode_signed_number(int(38.5 * 1E5)), '_p~iF')

    def data_test(self):
        test_data = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data.txt')

        for data, expected, threshold in _load_data(test_data):
            e = polyencoder.PolyEncoder(
                zoom_factor=expected['zoomFactor'], num_levels=expected['numLevels'], threshold=threshold)

            r = e.polyencode(data)

            self.assertEqual(r, expected['points'])


# more data


def _load_data(data_file):
    f = open(data_file, 'r')
    s = 0
    for line in f:
        if s == 0:
            data = []
            name = line.strip()
            reverse_coords = '(yx)' in name
            if '(t=' in name:
                threshold = float(re.search(r'\(t=(\d+\.\d+)\)', name).groups()[0])
            else:
                threshold = 0.00001
            s += 1
        elif s == 1:
            expected = json.loads(line.strip())
            s += 1
        elif s == 2 and len(line.strip()):
            coords = map(float, re.split('[, ]+', line.strip(), 2))
            if reverse_coords:
                coords.reverse()
            data.append(tuple(coords))
        else:
            s = 0
            yield name, data, expected, threshold
            data = []

    if len(data):
        yield name, data, expected, threshold


if __name__ == "__main__":
    import nose
    nose.main()
