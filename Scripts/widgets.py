from .configs import config

"""
Update the values of the keys in the dictionary.
"""

def Combobox(key, choice):
    config[key] = choice
    config.save()

def Switch(key, value):
    config[key] = value
    config.save()
