import mock
import pytest

from wykop.api.exceptions import WykopAPIError
from wykop.api.parsers.json import JSONParser


class TestJSONParserInit(object):

    def test_initialized(self):
        exception_resolver = mock.sentinel.exception_resolver
        json_param_name = 'json_param_name'
        json_param_value = 'json_param_value'
        json_params = {
            json_param_name: json_param_value,
        }

        parser = JSONParser(exception_resolver, **json_params)

        assert parser.exception_resolver == exception_resolver
        assert parser.json_kwargs == json_params


class TestJSONParserParse(object):

    @mock.patch.object(JSONParser, '_resolve_exception')
    @mock.patch('json.loads')
    def test_error(self, mocked_loads, mocked_resolve_exception, json_parser):
        data = mock.sentinel.data
        code = 1
        message = 'error message'
        response = {
            'error': {
                'code': code,
                'message': message,
            }
        }
        mocked_loads.return_value = response
        mocked_resolve_exception.side_effect = Exception()

        with pytest.raises(Exception):
            json_parser.parse(data)

        mocked_loads.assert_called_once_with(data, **json_parser.json_kwargs)
        mocked_resolve_exception.assert_called_once_with(
            code, message, WykopAPIError)

    @mock.patch.object(JSONParser, '_resolve_exception')
    @mock.patch('json.loads')
    def test_no_error(
            self, mocked_loads, mocked_resolve_exception, json_parser):
        data = mock.sentinel.data
        response = {
            'data': 'data'
        }
        mocked_loads.return_value = response

        result = json_parser.parse(data)

        mocked_loads.assert_called_once_with(data, **json_parser.json_kwargs)
        mocked_resolve_exception.assert_not_called()
        assert result == response
