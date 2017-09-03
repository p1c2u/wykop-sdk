"""Wykop API models module.."""
class WykopAPIResponse(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
