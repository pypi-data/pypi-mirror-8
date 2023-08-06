# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright © 2014 Tim Bielawa <timbielawa@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Test to verify the int/float/long conversions work correctly
"""

from . import TestCase
import bitmath
import sys

# Python 3.x compat
if sys.version > '3':
    long = int


class TestToBuiltInConversion(TestCase):

    def test_to_int(self):
        """int(bitmath) returns an int"""
        gib = bitmath.GiB(1337.8)
        self.assertIs(type(int(gib)), int)

    def test_to_float(self):
        """float(bitmath) returns a float"""
        gib = bitmath.GiB(1337.8)
        self.assertIs(type(float(gib)), float)

    def test_to_long(self):
        """long(bitmath) returns a long"""
        gib = bitmath.GiB(1337.8)
        self.assertIs(type(long(gib)), long)
