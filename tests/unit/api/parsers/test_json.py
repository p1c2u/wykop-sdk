import mock

from wykop.api.parsers.base import Error
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


class TestJSONParserGetResponse(object):

    @mock.patch('wykop.api.parsers.json.json.loads')
    def test_response(self, mock_loads, json_parser):
        data = mock.sentinel.data
        response = mock.sentinel.response
        mock_loads.return_value = response

        result = json_parser._get_response(data)

        mock_loads.assert_called_once_with(data, **json_parser.json_kwargs)
        assert result == response


class TestJSONParserGetError(object):

    def test_not_dict(self, json_parser):
        response = []

        result = json_parser._get_error(response)

        assert result is None

    def test_no_error(self, json_parser):
        response = {
            'data': 'data',
        }

        result = json_parser._get_error(response)

        assert result is None

    def test_error(self, json_parser):
        code = mock.sentinel.code
        message = mock.sentinel.message
        response = {
            'error': {
                'code': code,
                'message': message,
            }
        }

        result = json_parser._get_error(response)

        assert result == Error(code, message)
