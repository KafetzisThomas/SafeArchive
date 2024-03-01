#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import unittest
import datetime
from unittest.mock import patch
from Scripts.file_utils import backup_expiry_date


class TestBackupExpiryDate(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_destination'
        os.makedirs(self.test_dir, exist_ok=True)

    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('Scripts.file_utils.config', {'backup_expiry_date': '1 month'})


    def test_backup_expiry_date(self, mock_remove, mock_getmtime, mock_listdir):
        mock_listdir.return_value = ['backup1.zip', 'backup2.zip']

        # Set modification times for files to be older than expiry date
        mock_getmtime.side_effect = [
            datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(days=31)),
            datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(days=91))
        ]

        backup_expiry_date(self.test_dir)
        mock_remove.assert_any_call(os.path.join(self.test_dir, 'backup1.zip'))
        mock_remove.assert_any_call(os.path.join(self.test_dir, 'backup2.zip'))


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
