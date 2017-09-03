"""Wykop API exceptions resolver module."""
import sys

from wykop.utils import force_bytes


class ExceptionResolver(object):
    """Wykop API exception resolver."""

    def __init__(self, exceptions):
        self.exceptions = exceptions

    def get_class(self, code, default):
        return self.exceptions.get(code, default)

    def get_message(self, message):
        encoding = getattr(sys.stdout, 'encoding', 'utf-8')
        return force_bytes(message, encoding)

    def resolve(self, code, msg, default_class):
        klass = self.get_class(code, default_class)
        message = self.get_message(msg)
        return klass(message)
