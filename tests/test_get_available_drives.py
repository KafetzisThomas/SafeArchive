#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
import platform
import psutil
from Scripts.file_utils import get_available_drives


class MockDiskPartition:
    def __init__(self, device, mountpoint):
        self.device = device
        self.mountpoint = mountpoint


class TestGetAvailableDrives(unittest.TestCase):

    def test_get_available_drives_on_windows(self):
        if platform.system() == "Windows":
            # Mocking disk partitions for Windows
            psutil.disk_partitions = lambda: [
                MockDiskPartition('C:\\', 'C:/'), MockDiskPartition('D:\\', 'D:/')]

            drives = get_available_drives()
            self.assertEqual(drives, ['C:/', 'D:/'])


    def test_get_available_drives_on_linux(self):
        if platform.system() == "Linux":
            # Mocking disk partitions for Linux
            psutil.disk_partitions = lambda: [
                MockDiskPartition('/dev/sda1', '/media/usb1'), MockDiskPartition('/dev/sdb1', '/run/media/usb2')]

            drives = get_available_drives()
            self.assertEqual(drives, ['/media/usb1/', '/run/media/usb2/'])


if __name__ == '__main__':
    unittest.main()
