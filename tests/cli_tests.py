#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of polyencode.
# https://github.com/fitnr/polyencode

# Licensed under the GNU General Public License v3 (GPLv3) license:
# http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>
from __future__ import unicode_literals
import unittest
import os
import subprocess


class CliTestCase(unittest.TestCase):

    def setUp(self):
        geojson = os.path.join(os.path.dirname(__file__), 'fixtures', 'brooklyn.geojson')

        self.args = ['polyencode', 'layer', 'GEOID', geojson]
        self.geoid = '36047'.encode('utf8')

    def testPolyEncodePoints(self):
        args = ('polyencode', 'points', '41.87519,-87.67879', '41.86394,-87.63004')

        expected = 'vfzuOspo%7EF\n'.encode('utf8')

        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()

        self.assertIsNotNone(out)

        self.assertEqual(expected, out)

    def testPolyEncodePointsStdin(self):
        args = ('polyencode', 'points')
        points = b'41.87519,-87.67879 41.86394,-87.63004\n'
        expected = 'vfzuOspo%7EF\n'.encode('utf8')

        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate(points)

        self.assertIsNotNone(out)
        self.assertEqual(expected, out)


    def testPolyEncode(self):
        p = subprocess.Popen(self.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, _ = p.communicate()

        self.assertIsNotNone(out)

        expected = 'e%7B%7EvF%7Cc_cMi%7CBqCgI%7DEyAw%40IGcGcDgVeLgHqDsDkC_h'.encode('utf8')

        self.assertIn(self.geoid, out)
        self.assertIn('\t'.encode('utf8'), out)
        self.assertIn(expected, out)

    def testPolyEncodeNoUrlEncode(self):
        args = self.args + ['--no-encode']
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()

        expected = 'e{~vF|c_cMi|BqCgI}EyAw@IGcGcDgVeL'.encode('utf8')

        self.assertIsNotNone(out)

        self.assertIn(self.geoid, out)
        self.assertIn('\t'.encode('utf8'), out)
        self.assertIn(expected, out)

    def testPolyEncodePluralKeys(self):
        self.args[2] = 'GEOID,NAMELSAD'
        p = subprocess.Popen(self.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()

        self.assertIsNotNone(out)

        self.assertIn('Kings County'.encode('utf8'), out)

    def testPolyEncodeDelimiter(self):
        args = self.args + ['--delimiter', '|']
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()

        self.assertIsNotNone(out)

        self.assertIn('|'.encode('utf8'), out)

if __name__ == '__main__':
    unittest.main()
