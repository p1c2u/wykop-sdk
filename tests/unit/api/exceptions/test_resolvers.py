# -*- encoding: utf-8 -*-
import mock
import pytest

from six import b, text_type as u, binary_type

from wykop.api.exceptions.resolvers import ExceptionResolver


class MockStdout(object):

    def __init__(self, encoding=None):
        if encoding is not None:
            self.encoding = encoding


class TestExceptionResolverInit(object):

    def test_initialized(self):
        exceptions = mock.sentinel.exceptions

        resolver = ExceptionResolver(exceptions)

        assert resolver.exceptions == exceptions


class TestExceptionResolverGetClass(object):

    def test_existing(self, exception_resolver):
        code, klass = list(exception_resolver.exceptions.items())[0]
        test_class = type('TestException', (object,), {})

        result = exception_resolver.get_class(code, test_class)

        assert result == klass
        assert result != test_class

    def test_default(self, exception_resolver):
        code = 999
        test_class = type('TestException', (object,), {})

        result = exception_resolver.get_class(code, test_class)

        assert result == test_class


class TestExceptionResolverGetMessage(object):

    @pytest.mark.parametrize('message, expected', [
        (u'\u0105\u015b\u017c\u017amessage',
            b'\xc4\x85\xc5\x9b\xc5\xbc\xc5\xbamessage'),
        (b'\xc4\x85\xc5\x9b\xc5\xbc\xc5\xbamessage',
            b'\xc4\x85\xc5\x9b\xc5\xbc\xc5\xbamessage'),
    ])
    @mock.patch('sys.stdout', MockStdout())
    def test_no_stdout_encoding(self, message, expected, exception_resolver):
        result = exception_resolver.get_message(message)

        assert type(result) == binary_type
        assert result == expected

    @pytest.mark.parametrize('message, expected', [
        (u'\u0105\u015b\u017c\u017amessage',
            b'\xc4\x85\xc5\x9b\xc5\xbc\xc5\xbamessage'),
        (b'\xc4\x85\xc5\x9b\xc5\xbc\xc5\xbamessage',
            b'\xc4\x85\xc5\x9b\xc5\xbc\xc5\xbamessage'),
    ])
    @mock.patch('sys.stdout', MockStdout('utf-8'))
    def test_stdout_encoding(self, message, expected, exception_resolver):
        result = exception_resolver.get_message(message)

        assert type(result) == binary_type
        assert result == expected


class TestExceptionResolverResolve(object):

    @mock.patch.object(ExceptionResolver, 'get_message')
    @mock.patch.object(ExceptionResolver, 'get_class')
    def test_resolved(
            self, mocked_get_class, mocked_get_message, exception_resolver):
        code = mock.sentinel.code
        msg = mock.sentinel.msg
        default_class = mock.sentinel.default_class
        klass = type('TestClass', (object,), {'__init__': lambda x, y: None})
        message = mock.sentinel.message

        mocked_get_class.return_value = klass
        mocked_get_message.return_value = message

        result = exception_resolver.resolve(code, msg, default_class)

        mocked_get_class.assert_called_once_with(code, default_class)
        mocked_get_message.assert_called_once_with(msg)
        assert type(result) == klass
