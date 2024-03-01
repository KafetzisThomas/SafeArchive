#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import unittest
from Scripts.file_utils import get_backup_size


class TestGetBackupSize(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_backup_dir'
        os.makedirs(self.test_dir, exist_ok=True)

        with open(os.path.join(self.test_dir, 'test_file1.txt'), 'w') as f1:
            f1.write('Test content for file 1')

        with open(os.path.join(self.test_dir, 'test_file2.txt'), 'w') as f2:
            f2.write('Test content for file 2')


    def test_get_backup_size(self):
        backup_size = get_backup_size(self.test_dir)
        self.assertEqual(backup_size, os.path.getsize(os.path.join(self.test_dir, 'test_file1.txt')) + os.path.getsize(os.path.join(self.test_dir, 'test_file2.txt')))


    def tearDown(self):
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()
