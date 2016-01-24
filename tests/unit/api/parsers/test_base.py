import mock
import pytest

from wykop.api.exceptions.resolvers import ExceptionResolver
from wykop.api.parsers.base import BaseParser


class TestBaseParserInit(object):

    def test_initialized(self):
        exception_resolver = mock.sentinel.exception_resolver

        parser = BaseParser(exception_resolver)

        assert parser.exception_resolver == exception_resolver


class TestBaseParserResolveException(object):

    @mock.patch.object(ExceptionResolver, 'resolve')
    def test_exception(self, mocked_resolve, base_parser):
        code = mock.sentinel.code
        message = mock.sentinel.message
        default_class = mock.sentinel.default_class
        resolved = mock.sentinel.resolved
        mocked_resolve.return_value = resolved

        result = base_parser._resolve_exception(code, message, default_class)

        mocked_resolve.assert_called_once_with(code, message, default_class)
        assert result == resolved


class TestBaseParserParse(object):

    def test_raises_not_implemented(self, base_parser):
        data = mock.sentinel.data

        with pytest.raises(NotImplementedError):
            base_parser.parse(data)
