"""Python library for the Wykop API."""
from wykop.api.v1.clients import WykopAPIv1 as WykopAPI
from wykop.api.v2.clients import WykopAPIv2
from wykop.api.exceptions import WykopAPIError
from wykop.utils import get_version

__version__ = get_version()
