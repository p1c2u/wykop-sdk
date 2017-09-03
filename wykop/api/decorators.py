"""Wykop API decorators module."""
from wykop.api.exceptions import InvalidUserKeyError


def login_required(method):
    def decorator(self, *args, **kwargs):
        if not self.userkey:
            self.authenticate()

        try:
            return method(self, *args, **kwargs)
        # get new userkey on invalid key
        except InvalidUserKeyError:
            self.authenticate()
            return method(self, *args, **kwargs)
    return decorator
