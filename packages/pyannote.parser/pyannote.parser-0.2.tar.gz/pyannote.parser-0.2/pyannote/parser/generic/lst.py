#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2012-2014 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS: Hervé BREDIN - http://herve.niderb.fr

from __future__ import unicode_literals

from pyannote.parser.base import Parser


class LSTParser(Parser):
    """
    LST (list) is a dummy file format to specify a list of "things"
    (one thing per line)
    """

    @classmethod
    def file_extensions(cls):
        return ['lst']

    def empty(self, **kwargs):
        raise NotImplementedError()

    def read(self, path, **kwargs):
        """

        Parameters
        ----------
        path : str
            Path to list file (.lst)

        Returns
        -------
        lines : list
            List of stripped lines
        """

        with open(path, 'r') as f:
            lines = [line.strip() for line in f]

        self._loaded = lines

        return lines

    def __call__(self, **kwargs):
        return self._loaded
