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

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr

from __future__ import unicode_literals

from pyannote.core import Segment, Unknown
from pyannote.core import PYANNOTE_URI, PYANNOTE_MODALITY, PYANNOTE_LABEL

from base import AnnotationParser


class REPERELabelConverter(object):
    """Label converter

    Converts 'unknown' labels to Unknown instances while preserving others.

    Usage
    -----

    >>> Unknown.reset()
    >>> converter = REPERELabelConverter()
    >>> converter('Nicolas_SARKOZY')
    'Nicolas_SARKOZY'
    >>> converter('Inconnu_123')
    #1
    >>> converter('speaker#23')
    #2
    """

    def __init__(self):
        super(REPERELabelConverter, self).__init__()
        self.dict = {}

    def _unknown(self, label):
        # check whether `label` follows REPERE's unknown naming convention
        return label[:8] == 'Inconnu_' or label[:7] == 'speaker'

    def __call__(self, label):
        # convert label

        if label not in self.dict:

            # if label is unknown, create a new Unknown instance
            if self._unknown(label):
                self.dict[label] = Unknown()

            # if label is not unknown, add itself to internal dict
            else:
                self.dict[label] = label

        # return converted label
        return self.dict[label]

    def convert(self, annotation):
        mapping = {label: self(label) for label in annotation.labels()}
        return annotation.translate(mapping)


class REPEREParser(AnnotationParser):
    """REPERE file format"""

    @classmethod
    def file_extensions(cls):
        return ['repere', 'hyp']

    def fields(self):
        return [PYANNOTE_URI,
                'start',
                'end',
                PYANNOTE_MODALITY,
                PYANNOTE_LABEL]

    def comment(self):
        return ';'

    def converters(self):
        return {PYANNOTE_LABEL: REPERELabelConverter()}

    def get_segment(self, row):
        return Segment(row['start'], row['end'])

    def _append(self, annotation, f, uri, modality):

        try:
            format = '%s %%g %%g %s %%s\n' % (uri, modality)
            for segment, track, label in annotation.itertracks(label=True):
                f.write(format % (segment.start, segment.end, label))

        except Exception, e:
            print "Error @ %s%s %s %s" % (uri, segment, track, label)
            raise e

    @staticmethod
    def get_show_name(uri):
        """Get show name from uri"""
        tokens = uri.split('_')
        channel = tokens[0]
        show = tokens[1]
        return channel + '_' + show
