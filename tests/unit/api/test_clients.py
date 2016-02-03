import mock
import pytest

import json

from wykop.api.clients import BaseWykopAPI, WykopAPI
from wykop.api.parsers import JSONParser
from wykop.api.requesters import Requester


class TestBaseWykopAPIInit(object):

    def test_default(self):
        appkey = mock.sentinel.appkey
        secretkey = mock.sentinel.secretkey

        client = BaseWykopAPI(appkey, secretkey)

        assert client.appkey == appkey
        assert client.secretkey == secretkey
        assert client.login is None
        assert client.accountkey is None
        assert client.password is None
        assert client.output == ''
        assert client.format == 'json'

    def test_additional_options(self):
        appkey = mock.sentinel.appkey
        secretkey = mock.sentinel.secretkey
        login = mock.sentinel.login
        accountkey = mock.sentinel.accountkey
        password = mock.sentinel.password
        output = mock.sentinel.output
        response_format = mock.sentinel.response_format

        client = BaseWykopAPI(
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


class TestBaseWykopAPIGetMethodParams(object):

    def test_empty(self, base_wykop_api):
        method_params = ()

        result = base_wykop_api.get_method_params(*method_params)

        assert result == ()

    @pytest.mark.parametrize('method_params,expected', [
        ((1, 2), ('1', '2')),
        ((1.0, 2.0), ('1.0', '2.0')),
        (('str', 'base'), ('str', 'base')),
        ((True, False), ('True', 'False')),
    ])
    def test_mapped(self, method_params, expected, base_wykop_api):

        result = base_wykop_api.get_method_params(*method_params)

        assert result == expected


class TestBaseWykopAPIGetApiParams(object):

    def test_empty(self, base_wykop_api):
        api_params = {}

        result = base_wykop_api.get_api_params(**api_params)

        for param in ['appkey', 'format', 'output', 'userkey']:
            value = getattr(base_wykop_api, param)
            param_encoded = "{0},{1}".format(param, value)
            assert param_encoded in result

    def test_mapped(self, base_wykop_api):
        api_key = 'api_key'
        api_value = 'api_value'
        api_params = {
            api_key: api_value,
        }

        result = base_wykop_api.get_api_params(**api_params)

        for param in ['appkey', 'format', 'output', 'userkey']:
            value = getattr(base_wykop_api, param)
            param_encoded = "{0},{1}".format(param, value)
            assert param_encoded in result

        for param, value in api_params.items():
            param_encoded = "{0},{1}".format(param, value)
            assert param_encoded in result


class TestBaseWykopAPIGetPath(object):

    @mock.patch.object(BaseWykopAPI, 'get_api_params')
    @mock.patch.object(BaseWykopAPI, 'get_method_params')
    def test_no_params(
            self, mock_get_method_params, mock_get_api_params, base_wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        mock_get_method_params.return_value = ()
        mock_get_api_params.return_value = ''

        result = base_wykop_api.get_path(request_type, request_method)

        assert result == '{0}/{1}/'.format(request_type, request_method)

    @mock.patch.object(BaseWykopAPI, 'get_api_params')
    @mock.patch.object(BaseWykopAPI, 'get_method_params')
    def test_method_params(
            self, mock_get_method_params, mock_get_api_params, base_wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        method_param1 = 'param1'
        method_param2 = 'param2'
        method_params = (method_param1, method_param2)
        mock_get_method_params.return_value = method_params
        mock_get_api_params.return_value = ''

        result = base_wykop_api.get_path(
            request_type, request_method, method_param1, method_param2)

        mock_get_method_params.assert_called_once_with(
            method_param1, method_param2)
        mock_get_api_params.assert_called_once_with()
        assert result == '{0}/{1}/{2}/{3}/'.format(
            request_type, request_method, method_param1, method_param2)

    @mock.patch.object(BaseWykopAPI, 'get_api_params')
    @mock.patch.object(BaseWykopAPI, 'get_method_params')
    def test_api_params(
            self, mock_get_method_params, mock_get_api_params, base_wykop_api):
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

        result = base_wykop_api.get_path(
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

    @mock.patch.object(BaseWykopAPI, 'get_api_params')
    @mock.patch.object(BaseWykopAPI, 'get_method_params')
    def test_method_and_api_params(
            self, mock_get_method_params, mock_get_api_params, base_wykop_api):
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

        result = base_wykop_api.get_path(
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


class TestBaseWykopAPIConstructUrl(object):

    @mock.patch.object(BaseWykopAPI, 'get_path')
    def test_no_params(self, mocked_set_path, base_wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        mocked_set_path.return_value = path

        result = base_wykop_api.construct_url(request_type, request_method)

        mocked_set_path.assert_called_once_with(request_type, request_method)
        assert result == '{0}://{1}/{2}'.format(
            base_wykop_api._protocol,
            base_wykop_api._domain,
            path,
        )

    @mock.patch.object(BaseWykopAPI, 'get_path')
    def test_method_params(self, mocked_set_path, base_wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        method_param1 = 'param1'
        method_param2 = 'param2'
        mocked_set_path.return_value = path

        result = base_wykop_api.construct_url(
            request_type, request_method, method_param1, method_param2)

        mocked_set_path.assert_called_once_with(
            request_type, request_method, method_param1, method_param2)
        assert result == '{0}://{1}/{2}'.format(
            base_wykop_api._protocol,
            base_wykop_api._domain,
            path,
        )

    @mock.patch.object(BaseWykopAPI, 'get_path')
    def test_api_params(self, mocked_set_path, base_wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        api_param1_value = 'param1_value'
        api_param2_value = 'param2_value'
        mocked_set_path.return_value = path

        result = base_wykop_api.construct_url(
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
            base_wykop_api._protocol,
            base_wykop_api._domain,
            path,
        )

    @mock.patch.object(BaseWykopAPI, 'get_path')
    def test_method_and_api_params(self, mocked_set_path, base_wykop_api):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        method_param1 = 'param1'
        method_param2 = 'param2'
        api_param_value = 'param_value'
        mocked_set_path.return_value = path

        result = base_wykop_api.construct_url(
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
            base_wykop_api._protocol,
            base_wykop_api._domain,
            path,
        )


class TestBaseWykopAPIGetPostParamsValues(object):

    def test_no_params(self, base_wykop_api):
        post_params = {}

        result = base_wykop_api.get_post_params_values(**post_params)

        assert result == []

    def test_params(self, base_wykop_api):
        post_params = {
            'param1': 'z',
            'param2': 'a',
        }

        result = base_wykop_api.get_post_params_values(**post_params)

        assert result == ['z', 'a']


class TestBaseWykopAPIGetApiSign(object):

    @mock.patch.object(BaseWykopAPI, 'get_post_params_values')
    def test_no_params(self, mocked_get_post_params_values, base_wykop_api):
        url = mock.sentinel.url
        post_params = {}
        mocked_get_post_params_values.return_value = []

        result = base_wykop_api.get_api_sign(url, **post_params)

        mocked_get_post_params_values.assert_called_once_with(**post_params)
        assert result == 'fab16da58887f16066e6f7fc585f6ea5'

    @mock.patch.object(BaseWykopAPI, 'get_post_params_values')
    def test_params(self, mocked_get_post_params_values, base_wykop_api):
        url = mock.sentinel.url
        post_param1_value = 'post_param1_value'
        post_param2_value = 'post_param2_value'
        post_params = {
            'post_param1_name': post_param1_value,
            'post_param2_name': post_param2_value,
        }
        mocked_get_post_params_values.return_value = [
            post_param1_value, post_param2_value]

        result = base_wykop_api.get_api_sign(url, **post_params)

        mocked_get_post_params_values.assert_called_once_with(**post_params)
        assert result == '168499bac18e90313e5b46bf9f21403c'


class TestBaseWykopAPIGetUserAgent(object):

    @mock.patch('wykop.api.clients.get_version')
    def test_user_agent(self, mocked_get_version, base_wykop_api):
        version = 'version'
        mocked_get_version.return_value = version

        result = base_wykop_api.get_user_agent()

        assert result == '{0}/{1}'.format(base_wykop_api._client_name, version)


class TestBaseWykopAPIGetHeaders(object):

    @mock.patch.object(BaseWykopAPI, 'get_user_agent')
    @mock.patch.object(BaseWykopAPI, 'get_api_sign')
    def test_no_params(
            self, mocked_get_api_sign, mocked_get_user_agent, base_wykop_api):
        url = mock.sentinel.url
        post_params = {}
        api_sign = 'apisign'
        user_agent = 'useragent'
        mocked_get_api_sign.return_value = api_sign
        mocked_get_user_agent.return_value = user_agent

        result = base_wykop_api.get_headers(url, **post_params)

        mocked_get_api_sign.assert_called_once_with(url, **post_params)
        mocked_get_user_agent.assert_called_once_with()
        assert result == {
            'apisign': api_sign,
            'User-Agent': user_agent,
        }


class TestBaseWykopAPIRequest(object):

    @mock.patch.object(JSONParser, 'parse')
    @mock.patch.object(Requester, 'make_request')
    @mock.patch.object(BaseWykopAPI, 'get_headers')
    @mock.patch.object(BaseWykopAPI, 'construct_url')
    def test_no_params(
            self,
            mocked_construct_url,
            mocked_get_headers,
            mocked_make_request,
            mocked_parse,
            base_wykop_api):
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

        result = base_wykop_api.request(request_type, request_method)

        data = {}
        files = {}
        mocked_make_request.assert_called_once_with(url, data, headers, files)
        mocked_parse.assert_called_once_with(response)
        assert result == response

    @mock.patch.object(JSONParser, 'parse')
    @mock.patch.object(Requester, 'make_request')
    @mock.patch.object(BaseWykopAPI, 'get_headers')
    @mock.patch.object(BaseWykopAPI, 'construct_url')
    def test_no_parser(
            self,
            mocked_construct_url,
            mocked_get_headers,
            mocked_make_request,
            mocked_parse,
            base_wykop_api):
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

        result = base_wykop_api.request(
            request_type, request_method, parser=None)

        data = {}
        files = {}
        mocked_make_request.assert_called_once_with(url, data, headers, files)
        mocked_parse.assert_not_called()
        assert result == response
