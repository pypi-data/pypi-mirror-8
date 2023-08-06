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

from geotiler.map import Map, _find_top_left_tile, _find_tiles

import unittest


class MapTestCase(unittest.TestCase):
    """
    Map unit tests.
    """
    def test_map_create_error_center_extent(self):
        """
        Test map instantiation error with center and extent
        """
        extent = (0, 0, 0, 0)
        center = (0, 0)
        map = self.assertRaises(ValueError, Map, extent=extent, center=center)


    def test_map_create_error_extent_size_zoom(self):
        """
        Test map instantiation error with extent, size and zoom
        """
        extent = (0, 0, 0, 0)
        size = (0, 0)
        zoom = 1
        map = self.assertRaises(
            ValueError, Map, extent=extent, size=size, zoom=zoom
        )


    def test_map_create_center_zoom_size(self):
        """
        Test map instantiation with center, zoom and size
        """
        center = 11.788137, 46.481832
        zoom = 17
        size = 512, 512
        map = Map(center=center, zoom=zoom, size=size)
        self.assertEqual((512, 512), map.size)
        self.assertEqual(17, map.zoom)

        expected = 11.785390377044687, 46.4799402452901, 11.790883541107167, 46.48372275323265
        self.assertEqual(expected, map.extent)
        self.assertAlmostEqual(11.788137, map.center[0], 6)
        self.assertAlmostEqual(46.481832, map.center[1], 6)

        self.assertEqual((69827, 46376), map.origin)
        self.assertEqual((-238, -194), map.offset)


    def test_map_create_extent_size(self):
        """
        Test map instantiation with extent and size
        """
        extent = 11.785390377044687, 46.4799402452901, 11.790883541107167, 46.48372275323265
        size = 512, 512
        map = Map(extent=extent, size=size)

        self.assertEqual((512, 512), map.size)
        self.assertEqual(17, map.zoom)
        self.assertEqual(extent, map.extent)
        self.assertAlmostEqual(11.788137, map.center[0], 6)
        self.assertAlmostEqual(46.481832, map.center[1], 6)

        self.assertEqual((69827, 46376), map.origin)
        self.assertEqual((-238, -194), map.offset)


    def test_map_create_extent_zoom(self):
        """
        Test map instantiation with extent and zoom
        """
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        self.assertEqual((472, 270), map.size)
        self.assertEqual(17, map.zoom)
        self.assertEqual(extent, map.extent)
        self.assertAlmostEqual(11.788137, map.center[0], 6)
        self.assertAlmostEqual(46.481832, map.center[1], 6)

        self.assertEqual((69827, 46376), map.origin)
        self.assertEqual((-238, -194), map.offset)


    def test_map_size_change_954_541(self):
        """
        Test changing map size (954x541)
        """
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size

        map.size = 945, 541

        self.assertEqual((945, 541), map.size)
        self.assertEqual(17, map.zoom) # zoom has not changed
        expected = 11.783073, 46.4798368, 11.7932010, 46.4838261
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEqual(v1, v2, 6)

        self.assertEqual((69827, 46376), map.origin)
        self.assertEqual((-238, -194), map.offset)


    def test_map_size_change_1908x1082(self):
        """
        Test changing map size (1908x1082)
        """
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size

        map.size = 1908, 1082

        self.assertEqual((1908, 1082), map.size)
        self.assertEqual(17, map.zoom) # zoom has not changed
        expected = 11.777902, 46.4778346, 11.7983723, 46.4858281
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEqual(v1, v2, 6)

        self.assertEqual((69827, 46376), map.origin)
        self.assertEqual((-238, -194), map.offset)


    def test_map_center_change(self):
        """
        Test changing map center
        """
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size

        delta = 4 * 1e-5
        map.center = 11.788136959075942 + delta, 46.481831532133 + delta

        self.assertEqual((472, 270), map.size)
        self.assertEqual(17, map.zoom)

        expected = 11.7856478, 46.480871, 11.790712, 46.482866
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEqual(v1, v2, 6, map.extent)

        self.assertEqual((69827, 46376), map.origin)
        self.assertEqual((-242, -189), map.offset)


    def test_map_zoom_change(self):
        """
        Test changing map zoom
        """
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size
        assert map.zoom == 17, map.zoom

        map.zoom = 16

        self.assertEqual((472, 270), map.size)
        self.assertEqual(16, map.zoom)

        expected = 11.780519, 46.481270, 11.790648, 46.485259
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEqual(v1, v2, 6, map.extent)

        self.assertEqual((34913, 23188), map.origin)
        self.assertEqual(16, map.zoom)
        self.assertEqual((-128, 0), map.offset)


    def test_map_extent_change(self):
        """
        Test changing map extent
        """
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size
        assert map.zoom == 17, map.zoom

        map.extent = 11.785590, 46.480830, 11.790680, 46.482840

        self.assertEqual((474, 272), map.size)
        self.assertEqual(17, map.zoom)

        self.assertEqual((69827, 46376), map.origin)
        self.assertEqual((-238, -194), map.offset)


    def test_map_corner_calculation(self):
        """
        Test calculation of map corner
        """
        center = 11.788137, 46.481832
        zoom = 17
        size = 3000, 3000
        map = Map(center=center, zoom=zoom, size=size)

        assert map.size == (3000, 3000), map.size
        assert map.zoom == 17, map.zoom
        assert map.origin == (69827, 46376), map.origin
        assert map.offset == (-238, -194), map.offset

        coord, corner = _find_top_left_tile(map)
        self.assertEqual(69822.000, coord[0])
        self.assertEqual(46370.000, coord[1])
        self.assertEqual((-18, -230), corner)


    def test_map_corner_calculation_12(self):
        """
        Test calculation of map corner (zoom 12)
        """
        center = 11.788137, 46.481832
        zoom = 12
        size = 2000, 2000
        map = Map(center=center, zoom=zoom, size=size)

        assert map.size == (2000, 2000), map.size
        assert map.zoom == 12, map.zoom
        assert map.origin == (2182, 1449), map.origin
        assert map.offset == (-31, -70), map.offset

        coord, corner = _find_top_left_tile(map)
        self.assertEqual(2178, coord[0], coord)
        self.assertEqual(1445, coord[1], coord)
        self.assertEqual((-55, -94), corner)


    def test_map_tiles(self):
        """
        Test map tiles calculation
        """
        center = 11.788137, 46.481832
        zoom = 17
        size = 300, 300
        map = Map(center=center, zoom=zoom, size=size)

        coord, corner = _find_top_left_tile(map)
        tiles = _find_tiles(map, coord, corner)

        self.assertEqual(4, len(tiles))

        assert map.origin == (69827, 46376), map.origin
        assert map.offset == (-238, -194), map.offset

        t1, t2, t3, t4 = tiles

        # first row
        self.assertEqual((69827, 46376), t1[0], t1[0])
        self.assertEqual((-88, -44), t1[1])

        self.assertEqual((69828, 46376), t2[0], t2[0])
        self.assertEqual((-88 + 256, -44), t2[1])

        # second row
        self.assertEqual((69827, 46377), t3[0], t3[0])
        self.assertEqual((-88, -44 + 256), t3[1])

        self.assertEqual((69828, 46377), t4[0], t4[0])
        self.assertEqual((-88 + 256, -44 + 256), t4[1])


    def test_rev_geocode(self):
        """
        Test map reverse geocode
        """
        location = -6.066, 53.386
        map = Map(center=location, zoom=15, size=(1000, 1000))
        pos = map.rev_geocode(map.center)
        self.assertEqual((500, 500), pos)


# vim: sw=4:et:ai
