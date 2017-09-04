import pytest

from wykop.api.v2.clients import WykopAPIv2


@pytest.fixture
def wykop_api_v2():
    return WykopAPIv2(
        'sentinel.appkey',
        'sentinel.secretkey',
        output='sentinel.output',
        response_format='sentinel.format',
    )
