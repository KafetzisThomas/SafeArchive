#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from Scripts.configs import config


def DrivesCombobox(choice):
    """Update the value of the key in the dictionary"""
    config['destination_path'] = choice


def CloudSwitch(cloud_switch_var):
    """
    Get switch position (True/False)
    Update the value of the key in the dictionary
    """
    switch_position = cloud_switch_var.get()
    config['backup_to_cloud'] = True if switch_position == "on" else False


def BackupExpiryDateCombobox(choice):
    """Update the value of the key in the dictionary"""
    config['backup_expiry_date'] = choice


def AppearanceModeCombobox(choice):
    """Update the value of the key in the dictionary"""
    config['appearance_mode'] = choice


def ColorThemeCombobox(choice):
    """Update the value of the key in the dictionary"""
    config['color_theme'] = choice


def NotificationSwitch(notifications_switch_var):
    """
    Get switch position (True/False)
    Update the value of the key in the dictionary
    """
    switch_position = notifications_switch_var.get()
    config['notifications'] = True if switch_position == "on" else False
