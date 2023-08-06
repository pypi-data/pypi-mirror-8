#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           vis
# Program Description:    Helps analyze music with computers.
#
# Filename:               analyzers_tests/test_repeat.py
# Purpose:                Tests for repeat-based indexers.
#
# Copyright (C) 2013, 2014 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------

# allow "no docstring" for everything
# pylint: disable=C0111
# allow "too many public methods" for TestCase
# pylint: disable=R0904


import unittest
from numpy import nan, isnan
import pandas
from vis.analyzers.indexers.repeat import FilterByRepeatIndexer


class TestRepeatIndexer(unittest.TestCase):
    def test_offset_1part_1a(self):
        """1 part with 0 length"""
        in_val = [pandas.Series()]
        expected = {'0': pandas.Series()}
        ind = FilterByRepeatIndexer(in_val)
        actual = ind.run()
        self.assertIsInstance(actual, pandas.DataFrame)
        actual = actual['repeat.FilterByRepeatIndexer']
        for i in expected:  # compare each Series
            self.assertSequenceEqual(list(expected[i].index), list(actual[i].index))
            self.assertSequenceEqual(list(expected[i].values), list(actual[i].values))

    def test_offset_1part_1b(self):
        """2 parts, one of which has 0 length"""
        in_val = [pandas.Series(),
                  pandas.Series(['a', 'b', 'c', 'd'], index=[0.0, 0.5, 1.0, 1.5])]
        expected = {'0': pandas.Series([nan, nan, nan, nan], index=[0.0, 0.5, 1.0, 1.5]),
                    '1': pandas.Series(['a', 'b', 'c', 'd'], index=[0.0, 0.5, 1.0, 1.5])}
        ind = FilterByRepeatIndexer(in_val)
        actual = ind.run()
        self.assertIsInstance(actual, pandas.DataFrame)
        actual = actual['repeat.FilterByRepeatIndexer']
        for i in expected:  # compare each Series
            if isinstance(expected[i].values[0], float) and isnan(expected[i].values[0]):
                # just for this test, which has a bunch of NaNs
                for each in actual[i].values:
                    self.assertTrue(isnan(each))
            else:
                self.assertSequenceEqual(list(expected[i].index), list(actual[i].index))
                self.assertSequenceEqual(list(expected[i].values), list(actual[i].values))

    def test_offset_1part_2(self):
        """input is expected output"""
        in_val = [pandas.Series(['a', 'b', 'c', 'd'], index=[0.0, 0.5, 1.0, 1.5])]
        expected = {'0': pandas.Series(['a', 'b', 'c', 'd'], index=[0.0, 0.5, 1.0, 1.5])}
        ind = FilterByRepeatIndexer(in_val)
        actual = ind.run()
        self.assertIsInstance(actual, pandas.DataFrame)
        actual = actual['repeat.FilterByRepeatIndexer']
        for i in expected:  # compare each Series
            self.assertSequenceEqual(list(expected[i].index), list(actual[i].index))
            self.assertSequenceEqual(list(expected[i].values), list(actual[i].values))

    def test_offset_1part_3(self):
        """remove a bunch at the end"""
        in_val = [pandas.Series(['a', 'b', 'c', 'd', 'd', 'd', 'd'],
                                index=[0.0, 0.5, 1.0, 1.5, 1.6, 1.7, 1.8])]
        expected = {'0': pandas.Series(['a', 'b', 'c', 'd'], index=[0.0, 0.5, 1.0, 1.5])}
        ind = FilterByRepeatIndexer(in_val)
        actual = ind.run()
        self.assertIsInstance(actual, pandas.DataFrame)
        actual = actual['repeat.FilterByRepeatIndexer']
        for i in expected:  # compare each Series
            self.assertSequenceEqual(list(expected[i].index), list(actual[i].index))
            self.assertSequenceEqual(list(expected[i].values), list(actual[i].values))

    def test_offset_1part_4(self):
        """remove a bunch at the beginning"""
        in_val = [pandas.Series(['a', 'a', 'a', 'b', 'c', 'd'],
                                index=[0.0, 0.1, 0.2, 0.5, 1.0, 1.5])]
        expected = {'0': pandas.Series(['a', 'b', 'c', 'd'], index=[0.0, 0.5, 1.0, 1.5])}
        ind = FilterByRepeatIndexer(in_val)
        actual = ind.run()
        self.assertIsInstance(actual, pandas.DataFrame)
        actual = actual['repeat.FilterByRepeatIndexer']
        for i in expected:  # compare each Series
            self.assertSequenceEqual(list(expected[i].index), list(actual[i].index))
            self.assertSequenceEqual(list(expected[i].values), list(actual[i].values))

    def test_offset_1part_5(self):
        """remove alternating things"""
        in_val = [pandas.Series(['a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'],
                                index=[0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75])]
        expected = {'0': pandas.Series(['a', 'b', 'c', 'd'], index=[0.0, 0.5, 1.0, 1.5])}
        ind = FilterByRepeatIndexer(in_val)
        actual = ind.run()
        self.assertIsInstance(actual, pandas.DataFrame)
        actual = actual['repeat.FilterByRepeatIndexer']
        for i in expected:  # compare each Series
            self.assertSequenceEqual(list(expected[i].index), list(actual[i].index))
            self.assertSequenceEqual(list(expected[i].values), list(actual[i].values))

    def test_offset_1part_6(self):
        """pseudo-random"""
        in_val = [pandas.Series(['d', 'd', 'a', 's', 's', 'd', 'f', 'a', 'f', 'f', 's', 'd',
                                 'f', 's', 'f', 'd', 's', 's', 'a', 's'],
                                index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                       17, 18, 19, 20])]
        expected = {'0': pandas.Series(['d', 'a', 's', 'd', 'f', 'a', 'f', 's', 'd', 'f', 's', 'f',
                                        'd', 's', 'a', 's'],
                                       index=[1, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19, 20])}
        ind = FilterByRepeatIndexer(in_val)
        actual = ind.run()
        self.assertIsInstance(actual, pandas.DataFrame)
        actual = actual['repeat.FilterByRepeatIndexer']
        for i in expected:  # compare each Series
            self.assertSequenceEqual(list(expected[i].index), list(actual[i].index))
            self.assertSequenceEqual(list(expected[i].values), list(actual[i].values))

    def test_offset_2parts_1(self):
        """pseudo-random, many parts"""
        in_val = [pandas.Series(['d', 'd', 'a', 's', 's', 'd', 'f', 'a', 'f', 'f', 's', 'd', 'f',
                                 's', 'f', 'd', 's', 's', 'a', 's'],
                                index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                                       18, 19, 20]),
                  pandas.Series(['d', 'd', 'a', 's', 's', 'd', 'f', 'a', 'f', 'f', 's', 'd', 'f',
                                 's', 'f', 'd', 's', 's', 'a', 's'],
                                index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                                       18, 19, 20])]
        expected = {'0': pandas.Series(['d', 'a', 's', 'd', 'f', 'a', 'f', 's', 'd', 'f', 's', 'f',
                                        'd', 's', 'a', 's'],
                                       index=[1, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19, 20]),
                    '1': pandas.Series(['d', 'a', 's', 'd', 'f', 'a', 'f', 's', 'd', 'f', 's', 'f',
                                        'd', 's', 'a', 's'],
                                       index=[1, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19, 20])}
        ind = FilterByRepeatIndexer(in_val)
        actual = ind.run()
        self.assertIsInstance(actual, pandas.DataFrame)
        actual = actual['repeat.FilterByRepeatIndexer']
        for i in expected:  # compare each Series
            self.assertSequenceEqual(list(expected[i].index), list(actual[i].index))
            self.assertSequenceEqual(list(expected[i].values), list(actual[i].values))

#--------------------------------------------------------------------------------------------------#
# Definitions                                                                                      #
#--------------------------------------------------------------------------------------------------#
REPEAT_INDEXER_SUITE = unittest.TestLoader().loadTestsFromTestCase(TestRepeatIndexer)
