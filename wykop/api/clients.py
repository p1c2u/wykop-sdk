"""Wykop API clients module."""
import base64
import hashlib
import logging
from datetime import date, timedelta
from itertools import cycle

from six.moves.urllib.parse import urlunparse, quote_plus

from wykop.api.decorators import login_required
from wykop.api.exceptions import WykopAPIError, DailtyRequestLimitError
from wykop.api.parsers import default_parser
from wykop.api.requesters import default_requester
from wykop.utils import (
    dictmap,
    paramsencode,
    force_bytes,
    force_text,
    get_version,
)

log = logging.getLogger(__name__)


class BaseWykopAPI(object):
    """
    Base Wykop API.
    """

    _client_name = 'wykop-sdk'

    def __init__(self, appkey, secretkey, login=None, accountkey=None,
                 password=None, output='', response_format='json'):
        self.appkey = appkey
        self.secretkey = secretkey
        self.login = login
        self.accountkey = accountkey
        self.password = password
        self.output = output
        self.format = response_format
        self.userkey = ''

    def __getstate__(self):
        return {
            'appkey': self.appkey,
            'secretkey': self.secretkey,
            'login': self.login,
            'accountkey': self.accountkey,
            'password': self.password,
            'output': self.output,
            'format': self.format,
            'userkey': self.userkey,
        }

    def __setstate__(self, state):
        self.appkey = state['appkey']
        self.secretkey = state['secretkey']
        self.login = state['login']
        self.accountkey = state['accountkey']
        self.password = state['password']
        self.output = state['output']
        self.format = state['format']
        self.userkey = state['userkey']

    def get_default_api_params(self):
        """
        Gets default api parameters.
        """
        return {
            'appkey': self.appkey,
            'format': self.format,
            'output': self.output,
            'userkey': self.userkey,
        }

    def get_api_sign(self, url, **post_params):
        """
        Gets request api sign.
        """
        post_params_values = self.get_post_params_values(**post_params)
        post_params_values_str = ",".join(post_params_values)
        post_params_values_bytes = force_bytes(post_params_values_str)
        url_bytes = force_bytes(url)
        secretkey_bytes = force_bytes(self.secretkey)
        return hashlib.md5(
            secretkey_bytes + url_bytes + post_params_values_bytes).hexdigest()

    def get_post_params_values(self, **post_params):
        """
        Gets post parameters values list. Required to api sign.
        """
        return [force_text(post_params[key])
                for key in sorted(post_params.keys())]

    def get_user_agent(self):
        """
        Gets User-Agent header.
        """
        client_version = get_version()
        return '/'.join([self._client_name, client_version])

    def get_headers(self, url, **post_params):
        """
        Gets request headers.
        """
        apisign = self.get_api_sign(url, **post_params)
        user_agent = self.get_user_agent()

        return {
            'apisign': apisign,
            'User-Agent': user_agent,
        }

    def get_connect_api_params(self, redirect_url=None):
        """
        Gets request api parameters for wykop connect.
        """
        apisign = self.get_api_sign(redirect_url)

        api_params = {
            'secure': apisign,
        }

        if redirect_url is not None:
            redirect_url_bytes = force_bytes(redirect_url)
            redirect_url_encoded = quote_plus(
                base64.b64encode(redirect_url_bytes))
            api_params.update({
                'redirect': redirect_url_encoded,
            })

        return api_params

    def get_connect_data(self, data, parser=default_parser):
        """
        Gets decoded data from wykop connect.
        """
        data_bytes = force_bytes(data)
        decoded = base64.decodestring(data_bytes)
        decoded_str = force_text(decoded)
        parsed = parser.parse(decoded_str)
        return parsed['appkey'], parsed['login'], parsed['token']
