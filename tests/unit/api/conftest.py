import pytest
try:
    from unittest import mock
except ImportError:
    import mock


from wykop.api.clients import BaseWykopAPI, WykopAPI
from wykop.api.exceptions.resolvers import ExceptionResolver


class Test1Exception(Exception):
    pass


class Test2Exception(Exception):
    pass


@pytest.fixture
def base_wykop_api():
    return BaseWykopAPI(
        mock.sentinel.appkey,
        mock.sentinel.secretkey,
        login=mock.sentinel.login,
        accountkey=mock.sentinel.accountkey,
        password=mock.sentinel.password,
        output=mock.sentinel.output,
        response_format=mock.sentinel.format,
    )


@pytest.fixture
def wykop_api():
    return WykopAPI(
        mock.sentinel.appkey,
        mock.sentinel.secretkey,
        output=mock.sentinel.output,
        response_format=mock.sentinel.format,
    )


@pytest.fixture
def exception_resolver():
    exceptions = {
        1: Test1Exception,
        2: Test2Exception,
    }
    return ExceptionResolver(exceptions)
