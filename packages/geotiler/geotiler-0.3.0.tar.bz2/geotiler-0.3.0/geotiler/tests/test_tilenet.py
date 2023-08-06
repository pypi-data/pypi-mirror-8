#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice (restored, based on setup.py file from
# https://github.com/stamen/modestmaps-py):
#
#   Copyright (C) 2007-2013 by Michal Migurski and other contributors
#   License: BSD
#

"""
Map tile downloading code unit tests.
"""

from functools import wraps

from geotiler.tilenet import TileDownloader

import unittest
from unittest import mock


class TileDownloaderTestCase(unittest.TestCase):
    """
    Map tile downloader base class unit tests.
    """
    def test_setting_cache(self):
        """
        Test tile downloader cache change

        Verify that TileDownloader.fetch_image default cache is removed on
        cache change.
        """
        downloader = TileDownloader()
        fetch_image = downloader.fetch_image
        fetch_image_orig = downloader.fetch_image.__wrapped__

        assert fetch_image != fetch_image_orig

        def cache(f):
            @wraps(f)
            def f1(): return None
            return f1

        downloader.set_cache(cache)
        self.assertEqual(fetch_image_orig, downloader.fetch_image.__wrapped__)


# vim: sw=4:et:ai
