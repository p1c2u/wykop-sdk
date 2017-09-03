"""Wykop API parsers module."""
from wykop.api.exceptions import default_exception_resolver
from wykop.api.parsers.json import JSONParser
from wykop.api.models import WykopAPIResponse

default_parser = JSONParser(
    default_exception_resolver,
    object_hook=WykopAPIResponse,
)
