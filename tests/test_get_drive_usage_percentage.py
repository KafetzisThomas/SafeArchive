import unittest
import psutil
from Scripts.file_utils import get_drive_usage_percentage


class MockDiskUsage:

    def __init__(self, used, total):
        self.used = used
        self.total = total

    @property
    def percent(self):
        return (self.used / self.total) * 100


class TestGetDriveUsagePercentage(unittest.TestCase):

    def test_get_drive_usage_percentage(self):
        config = {'destination_path': '/mocked/path'}
        psutil.disk_usage = lambda path: MockDiskUsage(50 * (1024**3), 100 * (1024**3))  # 50 GB used, 100 GB total

        drive_usage_percentage = get_drive_usage_percentage()
        self.assertEqual(drive_usage_percentage, 50.0)


if __name__ == '__main__':
    unittest.main()
