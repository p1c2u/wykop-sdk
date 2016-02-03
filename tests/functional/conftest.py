import pytest

from wykop.api.clients import BaseWykopAPI
from wykop.api.requesters.requests import RequestsRequester
from wykop.api.requesters.urllib import UrllibRequester


@pytest.fixture
def requests_requester():
    return RequestsRequester()


@pytest.fixture
def urllib_requester():
    return UrllibRequester()


@pytest.fixture
def base_wykop_api():
    appkey = '123456app'
    secretkey = '654321secret'
    api = BaseWykopAPI(appkey, secretkey)
    api._domain = 'api.test.com'
    return api
