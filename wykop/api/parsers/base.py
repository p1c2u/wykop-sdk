"""Wykop API base praser module."""
from collections import namedtuple

from wykop.api.exceptions import WykopAPIError

Error = namedtuple('Error', ['code', 'message'])


class BaseParser(object):

    def __init__(self, exception_resolver):
        self.exception_resolver = exception_resolver

    def _resolve_exception(self, code, message, default_class):
        return self.exception_resolver.resolve(code, message, default_class)

    def parse(self, data):
        response = self._get_response(data)
        error = self._get_error(response)

        if error:
            raise self._resolve_exception(
                error.code, error.message, WykopAPIError)

        return response

    def _get_response(self, data):
        raise NotImplementedError(
            "%s: `_get_response` method must be implemented" %
            self.__class__.__name__)

    def _get_error(self, response):
        raise NotImplementedError(
            "%s: `_get_error` method must be implemented" %
            self.__class__.__name__)
