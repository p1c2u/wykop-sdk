import pytest
try:
    from unittest import mock
except ImportError:
    import mock


from wykop.api.clients import BaseWykopAPI, WykopAPI


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
