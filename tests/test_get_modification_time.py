#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import unittest
from Scripts.file_utils import get_modification_time


class TestGetModificationTime(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_destination'
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file = 'test_file.txt'

        with open(os.path.join(self.test_dir, self.test_file), 'w') as f:
            f.write('Test content')

        self.file_path = os.path.join(self.test_dir, self.test_file)


    def test_get_modification_time(self):
        # Modify the file's modification time for testing
        modified_time = 1614555600  # March 1, 2021
        os.utime(self.file_path, (modified_time, modified_time))

        result = get_modification_time(self.test_file, self.test_dir)
        self.assertEqual(result, modified_time)


    def tearDown(self):
        if os.path.exists(self.test_dir):
            os.remove(self.file_path)
            os.rmdir(self.test_dir)


if __name__ == '__main__':
    unittest.main()
