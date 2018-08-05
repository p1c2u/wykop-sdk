"""Wykop API decorators module."""
from functools import wraps

from wykop.api.exceptions import InvalidUserKeyError


def login_required(method):
    """
        .. note:: Metoda wymaga uwierzytelnienia.
    """
    @wraps(method)
    def decorator(self, *args, **kwargs):
        if not self.userkey:
            self.authenticate()

        try:
            return method(self, *args, **kwargs)
        # get new userkey on invalid key
        except InvalidUserKeyError:
            self.authenticate()
            return method(self, *args, **kwargs)
    decorator.__doc__ = decorator.__doc__ or ""
    decorator.__doc__ += login_required.__doc__
    return decorator
