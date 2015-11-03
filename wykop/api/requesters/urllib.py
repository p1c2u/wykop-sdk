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
    Urllib requester class
    """

    def make_request(self, url, data, headers, files=None):
        log.debug(" Fetching url: `%s` (POST: %s, headers: `%s`)" %
                  (str(url), str(data), str(headers)))

        if files:
            raise NotImplementedError(
                "Install requests package to send files.")

        data_bytes = force_bytes(urlencode(data))
        req = Request(url, data_bytes, headers=headers)

        try:
            with contextlib.closing(urlopen(req)) as f:
                return force_text(f.read())
        except HTTPError as e:
            raise WykopAPIError(0, str(e.code))
        except URLError as e:
            raise WykopAPIError(0, str(e.reason))
