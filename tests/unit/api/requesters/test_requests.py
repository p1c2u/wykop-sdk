from collections import namedtuple

import mock
import pytest
from requests.exceptions import RequestException

from wykop.api.exceptions import WykopAPIError
from wykop.api.requesters.requests import RequestsRequester

MockFile = namedtuple('MockFile', ['name', ])


class TestRequestsRequesterMakeRequest(object):

    @pytest.mark.parametrize("data,files,method", [
        (None, None, 'GET'),
        ({'test': 'data'}, None, 'POST'),
        (None, {'testfile': MockFile('testfile')}, 'POST'),
        ({'test': 'data'},  {'testfile': MockFile('testfile')}, 'POST'),
    ])
    @mock.patch('wykop.api.requesters.requests.request')
    @mock.patch.object(RequestsRequester, '_get_method')
    @mock.patch.object(RequestsRequester, '_get_files')
    def test_raises_error(
            self,
            mock_get_files,
            mock_get_method,
            mocked_request,
            data,
            files,
            method,
            requests_requester):
        url = 'http://test.com/api/1'
        headers = {
            'header': 'header',
        }
        mock_get_files.return_value = files
        mock_get_method.return_value = method
        mocked_request.side_effect = RequestException()

        with pytest.raises(WykopAPIError):
            requests_requester.make_request(
                url, data=data, headers=headers, files=files)

        mocked_request.assert_called_once_with(
            method, url, data=data, headers=headers, files=files)
