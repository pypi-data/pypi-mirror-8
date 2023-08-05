# Python-bioformats is distributed under the GNU General Public
# License, but this file is licensed under the more permissive BSD
# license.  See the accompanying file LICENSE for details.
# 
# Copyright (c) 2009-2014 Broad Institute
# All rights reserved.

import exceptions
import os
import unittest

import javabridge
import bioformats

import bioformats.formatreader as formatreader
import bioformats.metadatatools as metadatatools
from bioformats import load_image, load_image_url
from bioformats import log4j
import urllib

class TestLoadUsingBioformats(unittest.TestCase):

    def setUp(self):
        javabridge.attach()
        log4j.basic_config()
        
    def tearDown(self):
        javabridge.detach()

    def test_load_using_bioformats(self):
        path = os.path.join(os.path.dirname(__file__), 'Channel1-01-A-01.tif')
        image, scale = load_image(path, rescale=False,
                                  wants_max_intensity=True)
        print image.shape
        
    def test_file_not_found(self):
        # Regression test of issue #6
        path = os.path.join(os.path.dirname(__file__), 'Channel5-01-A-01.tif')
        self.assertRaises(exceptions.IOError, 
                          lambda :load_image(path))

class TestLoadUsingBioformatsURL(unittest.TestCase):
    def setUp(self):
        javabridge.attach()
        log4j.basic_config()
        
    def tearDown(self):
        javabridge.detach()

    def test_01_01_open_file(self):
        path = os.path.join(os.path.dirname(__file__), 'Channel1-01-A-01.tif')
        url = "file:" + urllib.pathname2url(path).encode("utf-8")
        image, scale = load_image_url(
            url, rescale=False, wants_max_intensity=True)
        self.assertEqual(image.shape[0], 640)
        
    def test_01_02_open_http(self):
        url = "https://github.com/CellProfiler/python-bioformats"+\
            "/raw/master/bioformats/tests/Channel1-01-A-01.tif"
        image, scale = load_image_url(
            url, rescale=False, wants_max_intensity=True)
        self.assertEqual(image.shape[0], 640)

    def test_01_03_unicode_url(self):
        #
        # Regression test of issue #17: ensure that this does not
        # raise an exception when converting URL to string
        #
        path = os.path.join(os.path.dirname(__file__), 'Channel1-01-A-01.tif')
        url = u"file:" + urllib.pathname2url(path).encode("utf-8")
        image, scale = load_image_url(
            url, rescale=False, wants_max_intensity=True)
        self.assertEqual(image.shape[0], 640)
        
    
