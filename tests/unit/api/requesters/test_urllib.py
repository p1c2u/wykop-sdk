import mock
import pytest

from wykop.api.exceptions import WykopAPIError

from six.moves.urllib.error import HTTPError, URLError


class MockFile(object):

    def __init__(self, name):
        self.name = name

    def read(self):
        return self.name

    def readline(self):
        return self.name

    def close(self):
        return


class TestUrllibRequesterMakeReuqest(object):

    def test_files_raises_not_implemented(self, urllib_requester):
        url = 'http://test.com/api/1'
        files = {
            'file': 'file',
        }

        with pytest.raises(NotImplementedError):
            urllib_requester.make_request(url, files=files)

    @mock.patch('wykop.api.requesters.urllib.urlopen')
    def test_urlerror_raises_error(self, mocked_urlopen, urllib_requester):
        url = 'http://test.com/api/1'

        mocked_urlopen.side_effect = URLError(url)

        with pytest.raises(WykopAPIError):
            urllib_requester.make_request(url)

    @mock.patch('wykop.api.requesters.urllib.urlopen')
    def test_httperror_raises_error(self, mocked_urlopen, urllib_requester):
        url = 'http://test.com/api/1'
        code = 777
        msg = 'msg'
        hdrs = 'hdrs'
        fp = MockFile(url)

        mocked_urlopen.side_effect = HTTPError(url, code, msg, hdrs, fp)

        with pytest.raises(WykopAPIError):
            urllib_requester.make_request(url)
