import mock
import pytest

from wykop.api.exceptions import WykopAPIError
from wykop.api.exceptions.resolvers import ExceptionResolver
from wykop.api.parsers.base import BaseParser, Error


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

    @mock.patch.object(BaseParser, '_resolve_exception')
    @mock.patch.object(BaseParser, '_get_error')
    @mock.patch.object(BaseParser, '_get_response')
    def test_error(
            self,
            mock_get_response,
            mock_get_error,
            mock_resolve_exception,
            base_parser):
        data = mock.sentinel.data
        response = mock.sentinel.response
        error = Error(mock.sentinel.code, mock.sentinel.message)
        mock_get_response.return_value = response
        mock_get_error.return_value = error
        mock_resolve_exception.side_effect = WykopAPIError()

        with pytest.raises(WykopAPIError):
            base_parser.parse(data)

        mock_get_response.assert_called_once_with(data)
        mock_get_error.assert_called_once_with(response)
        mock_resolve_exception.assert_called_once_with(
            error.code, error.message, WykopAPIError)

    @mock.patch.object(BaseParser, '_resolve_exception')
    @mock.patch.object(BaseParser, '_get_error')
    @mock.patch.object(BaseParser, '_get_response')
    def test_no_error(
            self,
            mock_get_response,
            mock_get_error,
            mock_resolve_exception,
            base_parser):
        data = mock.sentinel.data
        response = mock.sentinel.response
        mock_get_response.return_value = response
        mock_get_error.return_value = None

        result = base_parser.parse(data)

        mock_get_response.assert_called_once_with(data)
        mock_get_error.assert_called_once_with(response)
        mock_resolve_exception.assert_not_called()
        assert result == response


class TestBaseParserGetResponse(object):

    def test_raises_not_implemented(self, base_parser):
        data = mock.sentinel.data

        with pytest.raises(NotImplementedError):
            base_parser._get_response(data)


class TestBaseParserGetError(object):

    def test_raises_not_implemented(self, base_parser):
        data = mock.sentinel.data

        with pytest.raises(NotImplementedError):
            base_parser._get_error(data)
