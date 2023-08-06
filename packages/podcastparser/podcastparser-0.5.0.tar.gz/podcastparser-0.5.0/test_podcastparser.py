# -*- coding: utf-8 -*-
#
# test_podcastparser: Test Runner for the podcastparser (2012-12-29)
# Copyright (c) 2012, 2013, 2014, Thomas Perl <m@thp.io>
# Copyright (c) 2013, Stefan Kögl <stefan@skoegl.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#


import os
import glob
import json

from nose.tools import assert_equal

import podcastparser

def test_rss_parsing():
    def test_parse_rss(rss_filename):
        basename, _ = os.path.splitext(rss_filename)
        json_filename = basename + '.json'

        # read parameters to podcastparser.parse() from a separate file
        param_filename = basename + '.param.json'
        params = {}
        if os.path.exists(param_filename):
            params = json.load(open(param_filename))

        expected = json.load(open(json_filename))
        parsed = podcastparser.parse('file://' + rss_filename,
                                     open(rss_filename), **params)

        assert_equal.__self__.maxDiff = None
        assert_equal(expected, parsed)

    for rss_filename in glob.glob(os.path.join('tests', 'data', '*.rss')):
        yield test_parse_rss, rss_filename
