#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
import psutil
from Scripts.file_utils import storage_media_free_space


class MockDiskUsage:
    def __init__(self, free):
        self.free = free

class TestStorageMediaFreeSpace(unittest.TestCase):

    def test_storage_media_free_space(self):
        psutil.disk_usage = lambda path: MockDiskUsage(50 * (1024**3))  # 50 GB of free space

        free_space = storage_media_free_space()
        self.assertEqual(free_space, 50.0)


if __name__ == '__main__':
    unittest.main()
