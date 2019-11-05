#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import whaTFRecordsWriter


class UnitTests(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(whaTFRecordsWriter)

    def test_project(self):
        self.assertTrue(False, "write more tests here")