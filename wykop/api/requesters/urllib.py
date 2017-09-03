"""wykop API urllib requester module."""
import contextlib
import logging

from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import Request, urlopen

from wykop.api.exceptions import WykopAPIError
from wykop.api.requesters.base import BaseRequester
from wykop.utils import force_bytes, force_text

log = logging.getLogger(__name__)


class UrllibRequester(BaseRequester):
    """
    Urllib Wykop API requester. Uses urllib module.
    """

    def make_request(self, url, data=None, headers=None, files=None):
        log.debug(
            " Fetching url: `%s` (data: %s, headers: `%s`)",
            str(url), str(data), str(headers),
        )

        if files:
            raise NotImplementedError(
                "Install requests package to send files.")

        if headers is None:
            headers = {}

        data_bytes = force_bytes(urlencode(data)) if data else None
        req = Request(url, data=data_bytes, headers=headers)

        try:
            with contextlib.closing(urlopen(req)) as resp:
                return force_text(resp.read())
        except HTTPError as ex:
            raise WykopAPIError(0, str(ex.code))
        except URLError as ex:
            raise WykopAPIError(0, str(ex.reason))
