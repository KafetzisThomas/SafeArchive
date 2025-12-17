from .configs import config

"""
Update the values of the keys in the dictionary.
"""

def Combobox(key, choice):
    config.set(key, choice)

def Switch(key, value):
    config.set(key, value)
