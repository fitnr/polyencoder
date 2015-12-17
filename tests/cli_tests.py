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

        self.points_args = ['polyencode', 'points']

        self.tract_quoted = b'elrnEjgfpUqCi%40iO%7DC%7EC%7DVmMqCeJmB%7EF%7Bd%40%7EClAfJxExDjB%7CDtBrGtC%7CC%60BlEvBlBv%40nBbAVKCvAOt%40kFjOmAtDaEbL%7BA%7CDyAY'
        self.tract_unquoted = b'elrnEjgfpUqCi@iO}C~C}VmMqCeJmB~F{d@~ClAfJxExDjB|DtBrGtC|C`BlEvBlBv@nBbAVKCvAOt@kFjOmAtDaEbL{A|DyAY'

        self.tract = ['-118.16582,34.01427', '-118.16561,34.01501', '-118.1655,34.01535', '-118.16539,34.01571', '-118.16509,34.01673',
                      '-118.16496,34.01715', '-118.16489,34.01738', '-118.16482,34.01761', '-118.16465,34.01758', '-118.1642,34.01749',
                      '-118.16384,34.01741', '-118.16332,34.0173', '-118.16292,34.01722', '-118.16258,34.01714', '-118.16197,34.01701',
                      '-118.16099,34.01681', '-118.16085,34.01724', '-118.16044,34.01856', '-118.16034,34.01887', '-118.16026,34.01912',
                      '-118.15987,34.02039', '-118.15971,34.02092', '-118.15929,34.02083', '-118.15861,34.02069', '-118.15837,34.02064',
                      '-118.15734,34.02042', '-118.15722,34.02039', '-118.15677,34.0203', '-118.15642,34.02022', '-118.1563,34.02019',
                      '-118.15618,34.02017', '-118.15591,34.02011', '-118.1555,34.02002', '-118.1552,34.01996', '-118.15428,34.01976',
                      '-118.15413,34.01973', '-118.154,34.0197', '-118.15387,34.01968', '-118.15365,34.01963', '-118.15404,34.01883',
                      '-118.15407,34.01879', '-118.15426,34.01847', '-118.15442,34.01821', '-118.15448,34.0181', '-118.15481,34.01756',
                      '-118.15513,34.01703', '-118.15522,34.01687', '-118.15564,34.01615', '-118.15567,34.0161', '-118.1559,34.01574',
                      '-118.15593,34.01569', '-118.15615,34.01533', '-118.15626,34.01515', '-118.15636,34.01498', '-118.15659,34.01456',
                      '-118.15672,34.01431', '-118.15701,34.01378', '-118.15709,34.01365', '-118.15724,34.01341', '-118.15734,34.01324',
                      '-118.1575,34.01298', '-118.15778,34.01249', '-118.1581,34.01195', '-118.15823,34.0117', '-118.15838,34.0114',
                      '-118.15872,34.01084', '-118.15866,34.01072', '-118.15881,34.01072', '-118.15897,34.01073', '-118.1591,34.01074',
                      '-118.15937,34.01082', '-118.16026,34.01122', '-118.16029,34.01124', '-118.16053,34.01135', '-118.16057,34.01136',
                      '-118.16199,34.012', '-118.1629,34.01239', '-118.16302,34.01245', '-118.16359,34.01271', '-118.16421,34.013',
                      '-118.165,34.01336', '-118.16505,34.01339', '-118.16595,34.01382', '-118.16582,34.01427']

    def testPolyEncodePoints(self):
        p = subprocess.Popen(self.points_args + self.tract, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()
        self.assertIsNotNone(out)
        try:
            self.assertEqual(self.tract_quoted, out.strip())
        except AssertionError:
            print(self.points_args + self.tract)
            print(_)
            raise

    def testPolyEncodePointsUnquoted(self):
        p = subprocess.Popen(self.points_args + self.tract + ['--no-encode'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()
        self.assertIsNotNone(out)
        self.assertEqual(self.tract_unquoted, out.strip())

    def testPolyEncodePointsStdin(self):
        points = (' '.join(self.tract)).encode('utf8')
        p = subprocess.Popen(self.points_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate(points)
        self.assertIsNotNone(out)
        self.assertEqual(self.tract_quoted, out.strip())

    def testPolyEncodePointsStdinUnquoted(self):
        points = (' '.join(self.tract)).encode('utf8')
        p = subprocess.Popen(self.points_args + ['--no-encode'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate(points)
        self.assertIsNotNone(out)
        self.assertEqual(self.tract_unquoted, out.strip())


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
