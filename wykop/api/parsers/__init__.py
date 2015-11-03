from wykop.api.exceptions import default_exception_resolver
from wykop.api.parsers.json import JSONParser
from wykop.models import AttrDict

default_parser = JSONParser(
    default_exception_resolver, object_hook=lambda x: AttrDict(x))
