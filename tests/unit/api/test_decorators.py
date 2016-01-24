from itertools import chain, cycle
import mock

from wykop.api.clients import WykopAPI
from wykop.api.decorators import login_required
from wykop.api.exceptions import InvalidUserKeyError


class TestLoginRequired(object):

    @mock.patch.object(WykopAPI, 'request')
    @mock.patch.object(WykopAPI, 'authenticate')
    def test_no_userkey(self, mocked_authenticate, mocked_request, wykop_api):
        request_type = mock.sentinel.request_type
        request_method = mock.sentinel.request_method
        response = mock.sentinel.response
        mocked_request.return_value = response

        decorated_method = login_required(wykop_api.request)
        result = decorated_method(wykop_api, request_type, request_method)

        mocked_authenticate.assert_called_once_with()
        mocked_request.assert_called_once_with(
            wykop_api, request_type, request_method)
        assert result == response

    @mock.patch.object(WykopAPI, 'request')
    @mock.patch.object(WykopAPI, 'authenticate')
    def test_invalid_userkey(
            self, mocked_authenticate, mocked_request, wykop_api):
        request_type = mock.sentinel.request_type
        request_method = mock.sentinel.request_method
        response = mock.sentinel.response
        wykop_api.userkey = 'invalid_userkey'
        mocked_request.side_effect = chain(
            [InvalidUserKeyError()],
            cycle([response]),
        )

        decorated_method = login_required(wykop_api.request)
        result = decorated_method(wykop_api, request_type, request_method)

        mocked_authenticate.assert_called_once_with()
        calls = [
            mock.call(wykop_api, request_type, request_method),
            mock.call(wykop_api, request_type, request_method),
        ]
        mocked_request.assert_has_calls(calls)
        assert result == response
