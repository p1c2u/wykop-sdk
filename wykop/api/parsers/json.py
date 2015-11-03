from __future__ import absolute_import
try:
    import simplejson as json
except ImportError:
    import json

from wykop.api.exceptions import WykopAPIError
from wykop.api.parsers.base import BaseParser


class JSONParser(BaseParser):

    def __init__(self, *args, **json_kwargs):
        super(JSONParser, self).__init__(*args)
        self.json_kwargs = json_kwargs

    def parse(self, data):
        result = json.loads(data, **self.json_kwargs)

        if 'error' in result:
            code = result['error']['code']
            message = result['error']['message']
            raise self._resolve_exception(code, message, WykopAPIError)

        return result
