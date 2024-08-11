#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from ..configs import config


def Combobox(key, choice):
    """
    Update the value of the key in the dictionary.
    """
    config[key] = choice


def Switch(key, switch_var):
    """
    Get switch position (True/False).
    Update the value of the key in the dictionary.
    """
    switch_position = switch_var.get()
    config[key] = True if switch_position == "on" else False
