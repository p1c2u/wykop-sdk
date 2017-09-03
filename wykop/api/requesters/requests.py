"""Wykop API requests requester module."""
from __future__ import absolute_import
import logging

from requests import request
from requests.exceptions import RequestException

from wykop.api.exceptions import WykopAPIError
from wykop.api.requesters.base import BaseRequester
from wykop.utils import dictmap, mimetype, force_text

log = logging.getLogger(__name__)


class RequestsRequester(BaseRequester):
    """
    Requests Wtkop API requester. Uses reqeusts module.
    """

    METHOD_GET = 'GET'
    METHOD_POST = 'POST'

    def make_request(self, url, data=None, headers=None, files=None):
        log.debug(
            " Fetching url: `%s` (data: %s, headers: `%s`)",
            str(url), str(data), str(headers),
        )
        try:
            files = self._get_files(files)
            method = self._get_method(data, files)
            resp = request(method, url, data=data, headers=headers, files=files)
            resp.raise_for_status()
            return force_text(resp.content)
        except RequestException as ex:
            raise WykopAPIError(0, str(ex))

    def _get_files(self, files):
        return dictmap(lambda x: (x.name, x, mimetype(x.name)), files)

    def _get_method(self, data, files):
        return self.METHOD_POST if data or files else self.METHOD_GET
