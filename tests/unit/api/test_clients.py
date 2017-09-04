import mock

from wykop.api.clients import BaseWykopAPI


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
