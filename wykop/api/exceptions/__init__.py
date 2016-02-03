from wykop.api.exceptions.base import *
from wykop.api.exceptions.base import __all_exceptions__
from wykop.api.exceptions.resolvers import ExceptionResolver

default_exception_resolver = ExceptionResolver(__all_exceptions__)
