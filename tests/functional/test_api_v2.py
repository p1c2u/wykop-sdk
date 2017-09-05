import json
import mock
import responses


class FileMock(object):

    def __init__(self, name):
        self.name = name

    def read(self):
        return self.name

    def close(self):
        return


class TestWykopAPIv2(object):

    @responses.activate
    def test_simple(self, wykop_api_v2):
        rtype = 'rtype'
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey/123456app/format/json'
        url = '{protocol}://{domain}/{rtype}/{api_params}'.format(
            protocol=wykop_api_v2._protocol,
            domain=wykop_api_v2._domain,
            rtype=rtype,
            api_params=api_params,
        )
        responses.add(
            responses.GET,
            url,
            body=body,
            status=200,
            content_type='application/json',
        )

        response = wykop_api_v2.request(rtype)

        assert response == body_dict

    @responses.activate
    def test_rmethod(self, wykop_api_v2):
        rtype = 'rtype'
        rmethod = 'rmethod'
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey/123456app/format/json'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=wykop_api_v2._protocol,
            domain=wykop_api_v2._domain,
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

        response = wykop_api_v2.request(rtype, rmethod)

        assert response == body_dict

    @responses.activate
    def test_api_params(self, wykop_api_v2):
        rtype = 'rtype'
        rmethod = 'rmethod'
        api_params_dict = {
            'page': '2',
        }
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'page/2/appkey/123456app/format/json'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=wykop_api_v2._protocol,
            domain=wykop_api_v2._domain,
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

        response = wykop_api_v2.request(
            rtype, rmethod, api_params=api_params_dict)

        assert response == body_dict

    @responses.activate
    def test_post_params(self, wykop_api_v2):
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

        api_params = 'appkey/123456app/format/json'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=wykop_api_v2._protocol,
            domain=wykop_api_v2._domain,
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

        response = wykop_api_v2.request(
            rtype, rmethod, post_params=post_params)

        assert response == body_dict

    @responses.activate
    def test_file_params(self, wykop_api_v2):
        rtype = 'rtype'
        rmethod = 'rmethod'
        file_param_name = 'file_param_name'
        file_params = {
            file_param_name: FileMock(file_param_name),
        }
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey/123456app/format/json'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=wykop_api_v2._protocol,
            domain=wykop_api_v2._domain,
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

        response = wykop_api_v2.request(
            rtype, rmethod, file_params=file_params)

        assert response == body_dict

    @responses.activate
    def test_no_parser(self, wykop_api_v2):
        rtype = 'rtype'
        rmethod = 'rmethod'
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)

        api_params = 'appkey/123456app/format/json'
        url = '{protocol}://{domain}/{rtype}/{rmethod}/{api_params}'.format(
            protocol=wykop_api_v2._protocol,
            domain=wykop_api_v2._domain,
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

        response = wykop_api_v2.request(rtype, rmethod, parser=None)

        assert response == body

    @mock.patch('wykop.api.requesters.urllib.urlopen')
    def test_urllib_requester(
            self, mocked_urlopen, wykop_api_v2, urllib_requester):
        rtype = 'rtype'
        rmethod = 'rmethod'
        body_dict = {
            'data': 'data'
        }
        body = json.dumps(body_dict)
        mocked_urlopen.return_value = FileMock(body)

        response = wykop_api_v2.request(
            rtype, rmethod, requester=urllib_requester)

        assert mocked_urlopen.called
        assert response == body_dict
