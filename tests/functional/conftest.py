import pytest

from wykop.api.v1.clients import WykopAPIv1
from wykop.api.requesters.requests import RequestsRequester
from wykop.api.requesters.urllib import UrllibRequester


@pytest.fixture
def requests_requester():
    return RequestsRequester()


@pytest.fixture
def urllib_requester():
    return UrllibRequester()


@pytest.fixture
def wykop_api():
    appkey = '123456app'
    secretkey = '654321secret'
    api = WykopAPIv1(appkey, secretkey)
    api._domain = 'api.test.com'
    return api
