import mock
import pytest

from wykop.api.exceptions import DailtyRequestLimitError
from wykop.api.parsers import JSONParser
from wykop.api.requesters import Requester
from wykop.api.v1.clients import WykopAPIv1 as WykopAPI


class TestWykopAPIGetMethodParams(object):

    def test_empty(self, wykop_api):
        method_params = ()

        result = wykop_api.get_method_params(*method_params)

        assert result == ()

    @pytest.mark.parametrize('method_params,expected', [
        ((1, 2), ('1', '2')),
        ((1.0, 2.0), ('1.0', '2.0')),
        (('str', 'base'), ('str', 'base')),
        ((True, False), ('True', 'False')),
    ])
    def test_mapped(self, method_params, expected, wykop_api):

        result = wykop_api.get_method_params(*method_params)

        assert result == expected


class TestWykopAPIGetApiParams(object):

    def test_empty(self, wykop_api):
        api_params = {}

        result = wykop_api.get_api_params(**api_params)

        for param in ['appkey', 'format', 'output', 'userkey']:
            value = getattr(wykop_api, param)
            param_encoded = "{0},{1}".format(param, value)
            assert param_encoded in result

    def test_mapped(self, wykop_api):
        api_key = 'api_key'
        api_value = 'api_value'
        api_params = {
            api_key: api_value,
        }

        result = wykop_api.get_api_params(**api_params)

        for param in ['appkey', 'format', 'output', 'userkey']:
            value = getattr(wykop_api, param)
            param_encoded = "{0},{1}".format(param, value)
            assert param_encoded in result

        for param, value in api_params.items():
            param_encoded = "{0},{1}".format(param, value)
            assert param_encoded in result


class TestWykopAPIGetPath(object):

    @mock.patch.object(WykopAPI, 'get_api_params')
    @mock.patch.object(WykopAPI, 'get_method_params')
    def test_no_params(
            self, mock_get_method_params, mock_get_api_params, wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        mock_get_method_params.return_value = ()
        mock_get_api_params.return_value = ''

        result = wykop_api.get_path(request_type, request_method)

        assert result == '{0}/{1}/'.format(request_type, request_method)

    @mock.patch.object(WykopAPI, 'get_api_params')
    @mock.patch.object(WykopAPI, 'get_method_params')
    def test_method_params(
            self, mock_get_method_params, mock_get_api_params, wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        method_param1 = 'param1'
        method_param2 = 'param2'
        method_params = (method_param1, method_param2)
        mock_get_method_params.return_value = method_params
        mock_get_api_params.return_value = ''

        result = wykop_api.get_path(
            request_type, request_method, method_param1, method_param2)

        mock_get_method_params.assert_called_once_with(
            method_param1, method_param2)
        mock_get_api_params.assert_called_once_with()
        assert result == '{0}/{1}/{2}/{3}/'.format(
            request_type, request_method, method_param1, method_param2)

    @mock.patch.object(WykopAPI, 'get_api_params')
    @mock.patch.object(WykopAPI, 'get_method_params')
    def test_api_params(
            self, mock_get_method_params, mock_get_api_params, wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        api_param1_name = 'api_param1_name'
        api_param1_value = 'api_param1_value'
        api_param2_name = 'api_param2_name'
        api_param2_value = 'api_param2_value'

        api_params = '{0},{1},{2},{3}'.format(
            api_param1_name,
            api_param1_value,
            api_param2_name,
            api_param2_value,
        )
        mock_get_method_params.return_value = ()
        mock_get_api_params.return_value = api_params

        result = wykop_api.get_path(
            request_type,
            request_method,
            api_param1_name=api_param1_value,
            api_param2_name=api_param2_value,
        )

        assert result == '{0}/{1}/{2}'.format(
            request_type,
            request_method,
            api_params,
        )

    @mock.patch.object(WykopAPI, 'get_api_params')
    @mock.patch.object(WykopAPI, 'get_method_params')
    def test_method_and_api_params(
            self, mock_get_method_params, mock_get_api_params, wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        method_param1 = 'param1'
        method_param2 = 'param2'
        api_param_name = 'api_param_name'
        api_param_value = 'api_param_value'

        method_params = (method_param1, method_param2)
        api_params = '{0},{1}'.format(api_param_name, api_param_value)
        mock_get_method_params.return_value = method_params
        mock_get_api_params.return_value = api_params

        result = wykop_api.get_path(
            request_type,
            request_method,
            method_param1,
            method_param2,
            api_param_name=api_param_value,
        )

        assert result == '{0}/{1}/{2}/{3}/{4}'.format(
            request_type,
            request_method,
            method_param1,
            method_param2,
            api_params,
        )


class TestWykopAPIInit(object):

    @mock.patch.object(WykopAPI, 'authenticate')
    def test_base_init(self, mocked_authenticate):
        appkey = mock.sentinel.appkey
        secretkey = mock.sentinel.secretkey
        login = mock.sentinel.login
        accountkey = mock.sentinel.accountkey
        password = mock.sentinel.password
        output = mock.sentinel.output
        response_format = mock.sentinel.response_format

        client = WykopAPI(
            appkey,
            secretkey,
            login=login,
            accountkey=accountkey,
            password=password,
            output=output,
            response_format=response_format,
        )

        assert client.appkey == appkey
        assert client.secretkey == secretkey
        assert client.login == login
        assert client.accountkey == accountkey
        assert client.password is password
        assert client.output == output
        assert client.format == response_format

    @mock.patch.object(WykopAPI, 'authenticate')
    def test_no_auth(self, mocked_authenticate):
        appkey = mock.sentinel.appkey
        secretkey = mock.sentinel.secretkey

        WykopAPI(appkey, secretkey)

        assert not mocked_authenticate.called

    @mock.patch.object(WykopAPI, 'authenticate')
    def test_auth_with_accountkey(self, mocked_authenticate):
        appkey = mock.sentinel.appkey
        secretkey = mock.sentinel.secretkey
        login = mock.sentinel.login
        accountkey = mock.sentinel.accountkey

        WykopAPI(appkey, secretkey, login=login, accountkey=accountkey)

        mocked_authenticate.assert_called_once_with()

    @mock.patch.object(WykopAPI, 'authenticate')
    def test_auth_with_password(self, mocked_authenticate):
        appkey = mock.sentinel.appkey
        secretkey = mock.sentinel.secretkey
        login = mock.sentinel.login
        password = mock.sentinel.password

        WykopAPI(appkey, secretkey, login=login, password=password)

        mocked_authenticate.assert_called_once_with()


class TestWykopAPIConstructUrl(object):

    @mock.patch.object(WykopAPI, 'get_path')
    def test_no_params(self, mocked_set_path, wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        mocked_set_path.return_value = path

        result = wykop_api.construct_url(request_type, request_method)

        mocked_set_path.assert_called_once_with(request_type, request_method)
        assert result == '{0}://{1}/{2}'.format(
            wykop_api._protocol,
            wykop_api._domain,
            path,
        )

    @mock.patch.object(WykopAPI, 'get_path')
    def test_method_params(self, mocked_set_path, wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        method_param1 = 'param1'
        method_param2 = 'param2'
        mocked_set_path.return_value = path

        result = wykop_api.construct_url(
            request_type, request_method, method_param1, method_param2)

        mocked_set_path.assert_called_once_with(
            request_type, request_method, method_param1, method_param2)
        assert result == '{0}://{1}/{2}'.format(
            wykop_api._protocol,
            wykop_api._domain,
            path,
        )

    @mock.patch.object(WykopAPI, 'get_path')
    def test_api_params(self, mocked_set_path, wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        api_param1_value = 'param1_value'
        api_param2_value = 'param2_value'
        mocked_set_path.return_value = path

        result = wykop_api.construct_url(
            request_type,
            request_method,
            api_param1_name=api_param1_value,
            api_param2_name=api_param2_value,
        )

        mocked_set_path.assert_called_once_with(
            request_type,
            request_method,
            api_param1_name=api_param1_value,
            api_param2_name=api_param2_value,
        )
        assert result == '{0}://{1}/{2}'.format(
            wykop_api._protocol,
            wykop_api._domain,
            path,
        )

    @mock.patch.object(WykopAPI, 'get_path')
    def test_method_and_api_params(self, mocked_set_path, wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        method_param1 = 'param1'
        method_param2 = 'param2'
        api_param_value = 'param_value'
        mocked_set_path.return_value = path

        result = wykop_api.construct_url(
            request_type,
            request_method,
            method_param1,
            method_param2,
            api_param_name=api_param_value,
        )

        mocked_set_path.assert_called_once_with(
            request_type,
            request_method,
            method_param1,
            method_param2,
            api_param_name=api_param_value,
        )
        assert result == '{0}://{1}/{2}'.format(
            wykop_api._protocol,
            wykop_api._domain,
            path,
        )


class TestWykopAPIRequest(object):

    @mock.patch.object(JSONParser, 'parse')
    @mock.patch.object(Requester, 'make_request')
    @mock.patch.object(WykopAPI, 'get_headers')
    @mock.patch.object(WykopAPI, 'construct_url')
    def test_no_params(
            self,
            mocked_construct_url,
            mocked_get_headers,
            mocked_make_request,
            mocked_parse,
            wykop_api):
        request_type = mock.sentinel.request_type
        request_method = mock.sentinel.request_method
        url = 'testurl'
        headers = {
            'apisign': '932bab4abf55123e92bf878cd2b9cee4',
            'User-Agent': 'wykop-sdk/dev',
        }
        response = {}

        mocked_construct_url.return_value = url
        mocked_get_headers.return_value = headers
        mocked_make_request.return_value = response
        mocked_parse.return_value = response

        result = wykop_api.request(request_type, request_method)

        data = {}
        files = {}
        mocked_make_request.assert_called_once_with(url, data, headers, files)
        mocked_parse.assert_called_once_with(response)
        assert result == response

    @mock.patch.object(JSONParser, 'parse')
    @mock.patch.object(Requester, 'make_request')
    @mock.patch.object(WykopAPI, 'get_headers')
    @mock.patch.object(WykopAPI, 'construct_url')
    def test_no_parser(
            self,
            mocked_construct_url,
            mocked_get_headers,
            mocked_make_request,
            mocked_parse,
            wykop_api):
        request_type = mock.sentinel.request_type
        request_method = mock.sentinel.request_method
        url = 'testurl'
        headers = {
            'apisign': '932bab4abf55123e92bf878cd2b9cee4',
            'User-Agent': 'wykop-sdk/dev',
        }
        response = {}

        mocked_construct_url.return_value = url
        mocked_get_headers.return_value = headers
        mocked_make_request.return_value = response
        mocked_parse.return_value = response

        result = wykop_api.request(
            request_type, request_method, parser=None)

        data = {}
        files = {}
        mocked_make_request.assert_called_once_with(url, data, headers, files)
        mocked_parse.assert_not_called()
        assert result == response


class TestRotatingKeysWykopAPIRequest(object):

    @mock.patch.object(WykopAPI, 'request')
    def test_no_rotate_keys(self, mocked_request, rotating_keys_wykop_api):
        request_type = mock.sentinel.request_type
        request_method = mock.sentinel.request_method
        response = mock.sentinel.response
        mocked_request.return_value = response
        first_appkey = rotating_keys_wykop_api.appkey
        first_secretkey = rotating_keys_wykop_api.secretkey

        result = rotating_keys_wykop_api.request(request_type, request_method)

        mocked_request.assert_called_once_with(request_type, request_method)
        assert result == response
        assert rotating_keys_wykop_api.appkey == first_appkey
        assert rotating_keys_wykop_api.secretkey == first_secretkey

    @mock.patch.object(WykopAPI, 'request')
    def test_rotate_keys(self, mocked_request, rotating_keys_wykop_api):
        request_type = mock.sentinel.request_type
        request_method = mock.sentinel.request_method
        response = mock.sentinel.response
        mocked_request.side_effect = [
            DailtyRequestLimitError(),
            response,
        ]
        first_appkey = rotating_keys_wykop_api.appkey
        first_secretkey = rotating_keys_wykop_api.secretkey

        result = rotating_keys_wykop_api.request(request_type, request_method)

        calls = [
            mock.call(request_type, request_method),
        ]
        mocked_request.assert_has_calls(calls)
        assert result == response
        assert not rotating_keys_wykop_api.appkey == first_appkey
        assert not rotating_keys_wykop_api.secretkey == first_secretkey

    @mock.patch.object(WykopAPI, 'request')
    def test_rotate_keys_repeat(self, mocked_request, rotating_keys_wykop_api):
        request_type = mock.sentinel.request_type
        request_method = mock.sentinel.request_method
        response = mock.sentinel.response
        mocked_request.side_effect = [
            DailtyRequestLimitError(),
            DailtyRequestLimitError(),
            response,
        ]
        first_appkey = rotating_keys_wykop_api.appkey
        first_secretkey = rotating_keys_wykop_api.secretkey

        result = rotating_keys_wykop_api.request(request_type, request_method)

        calls = [
            mock.call(request_type, request_method),
        ]
        mocked_request.assert_has_calls(calls)
        assert result == response
        assert rotating_keys_wykop_api.appkey == first_appkey
        assert rotating_keys_wykop_api.secretkey == first_secretkey
