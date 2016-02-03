import pytest

from wykop.api.requesters.base import BaseRequester
from wykop.api.requesters.requests import RequestsRequester
from wykop.api.requesters.urllib import UrllibRequester


@pytest.fixture
def base_requester():
    return BaseRequester()


@pytest.fixture
def requests_requester():
    return RequestsRequester()


@pytest.fixture
def urllib_requester():
    return UrllibRequester()
