import pytest

from wykop.api.exceptions.resolvers import ExceptionResolver


class Test1Exception(Exception):
    pass


class Test2Exception(Exception):
    pass


@pytest.fixture
def exception_resolver():
    exceptions = {
        1: Test1Exception,
        2: Test2Exception,
    }
    return ExceptionResolver(exceptions)
