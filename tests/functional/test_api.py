import json
import mock
import responses


class MockFile(object):

    def __init__(self, name):
        self.name = name

    def read(self):
        return self.name

    def close(self):
        return


class TestWykopAPI(object):

    @responses.activate
    def test_simple(self, base_wykop_api):
        rtype = 'rtype'
        rmethod = 'rmethod'
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey,123456app,format,json,output,,userkey,'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=base_wykop_api._protocol,
            domain=base_wykop_api._domain,
            rtype=rtype,
            rmethod=rmethod,
            api_params=api_params,
        )
        responses.add(
            responses.GET,
            url,
            body=body,
            status=200,
            content_type='application/json',
        )

        response = base_wykop_api.request(rtype, rmethod)

        assert response == body_dict

    @responses.activate
    def test_rmethod_params(self, base_wykop_api):
        rtype = 'rtype'
        rmethod = 'rmethod'
        rmethod_param = 'rmethod_param'
        rmethod_params = [rmethod_param, ]
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey,123456app,format,json,output,,userkey,'
        url = ('{protocol}://{domain}/{rtype}/{rmethod}/'
               '{rmethod_param}/{api_params}').format(
            protocol=base_wykop_api._protocol,
            domain=base_wykop_api._domain,
            rtype=rtype,
            rmethod=rmethod,
            rmethod_param=rmethod_param,
            api_params=api_params,
        )
        responses.add(
            responses.GET,
            url,
            body=body,
            status=200,
            content_type='application/json',
        )

        response = base_wykop_api.request(
            rtype, rmethod, rmethod_params=rmethod_params)

        assert response == body_dict

    @responses.activate
    def test_api_params(self, base_wykop_api):
        rtype = 'rtype'
        rmethod = 'rmethod'
        api_params_dict = {
            'appkey': '321app',
            'format': 'zip',
            'output': 'nooutput',
            'userkey': '456key',
        }
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey,321app,format,zip,output,nooutput,userkey,456key'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=base_wykop_api._protocol,
            domain=base_wykop_api._domain,
            rtype=rtype,
            rmethod=rmethod,
            api_params=api_params,
        )
        responses.add(
            responses.GET,
            url,
            body=body,
            status=200,
            content_type='application/json',
        )

        response = base_wykop_api.request(
            rtype, rmethod, api_params=api_params_dict)

        assert response == body_dict

    @responses.activate
    def test_post_params(self, base_wykop_api):
        rtype = 'rtype'
        rmethod = 'rmethod'
        post_param_name = 'post_param_name'
        post_param_value = 'post_param_value'
        post_params = {
            post_param_name: post_param_value,
        }
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey,123456app,format,json,output,,userkey,'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=base_wykop_api._protocol,
            domain=base_wykop_api._domain,
            rtype=rtype,
            rmethod=rmethod,
            api_params=api_params,
        )
        responses.add(
            responses.POST,
            url,
            body=body,
            status=200,
            content_type='application/json',
        )

        response = base_wykop_api.request(
            rtype, rmethod, post_params=post_params)

        assert response == body_dict

    @responses.activate
    def test_file_params(self, base_wykop_api):
        rtype = 'rtype'
        rmethod = 'rmethod'
        file_param_name = 'file_param_name'
        file_params = {
            file_param_name: MockFile(file_param_name),
        }
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey,123456app,format,json,output,,userkey,'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=base_wykop_api._protocol,
            domain=base_wykop_api._domain,
            rtype=rtype,
            rmethod=rmethod,
            api_params=api_params,
        )
        responses.add(
            responses.POST,
            url,
            body=body,
            status=200,
            content_type='application/json',
        )

        response = base_wykop_api.request(
            rtype, rmethod, file_params=file_params)

        assert response == body_dict

    @responses.activate
    def test_no_parser(self, base_wykop_api):
        rtype = 'rtype'
        rmethod = 'rmethod'
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey,123456app,format,json,output,,userkey,'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=base_wykop_api._protocol,
            domain=base_wykop_api._domain,
            rtype=rtype,
            rmethod=rmethod,
            api_params=api_params,
        )
        responses.add(
            responses.GET,
            url,
            body=body,
            status=200,
            content_type='application/json',
        )

        response = base_wykop_api.request(rtype, rmethod, parser=None)

        assert response == body

    @mock.patch('wykop.api.requesters.urllib.urlopen')
    def test_urllib_requester(
            self, mocked_urlopen, base_wykop_api, urllib_requester):
        rtype = 'rtype'
        rmethod = 'rmethod'
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)
        mocked_urlopen.return_value = MockFile(body)

        response = base_wykop_api.request(
            rtype, rmethod, requester=urllib_requester)

        assert mocked_urlopen.called
        assert response == body_dict
