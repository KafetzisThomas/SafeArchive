#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import unittest
from Scripts.file_utils import create_destination_directory_path


class TestCreateDestinationDirectoryPath(unittest.TestCase):
    def setUp(self):
        self.destination_path = 'test_destination_path'

    def test_create_directory_if_not_exists(self):
        create_destination_directory_path(self.destination_path)
        self.assertTrue(os.path.exists(self.destination_path))

    def tearDown(self):
        if os.path.exists(self.destination_path):
            os.rmdir(self.destination_path)


if __name__ == '__main__':
    unittest.main()
