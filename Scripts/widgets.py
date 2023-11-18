#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from Scripts.configs import config


def drivesCombobox(choice):
    """Update the value of the key in the dictionary"""
    config['destination_path'] = choice


def cloudSwitch(cloud_switch_var):
    """
    Get switch position (True/False)
    Update the value of the key in the dictionary
    """
    switch_position = cloud_switch_var.get()
    config['backup_to_cloud'] = True if switch_position == "on" else False


def backupExpiryDateCombobox(choice):
    """Update the value of the key in the dictionary"""
    config['backup_expiry_date'] = choice
