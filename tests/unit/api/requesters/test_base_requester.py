import mock
import pytest


class TestBaseRequesterMakeRequest(object):

    def test_raises_not_implemented(self, base_requester):
        url = mock.sentinel.url
        data = mock.sentinel.data
        headers = mock.sentinel.headers
        files = mock.sentinel.files

        with pytest.raises(NotImplementedError):
            base_requester.make_request(
                url, data=data, headers=headers, files=files)
