# -*- coding: utf-8 -*-
import datetime
from pkg_resources import DistributionNotFound
import mock
import pytest

from six import b, u

from wykop.utils import force_text, force_bytes, get_version


class TestForceText(object):

    def test_text(self):
        result = force_text('test')

        assert result == 'test'

    def test_decoding(self):
        msg = b('cze\xc5\x9b\xc4\x87')

        result = force_text(msg)

        assert result == u('cze\u015b\u0107')

    def test_decoding_ignore(self):
        msg = b('cze\xc5\x9b\xc4\x87')

        result = force_text(msg, encoding='ascii', errors='ignore')

        assert result == u('cze')


class TestForceBytes(object):

    def test_exception(self):
        error_msg = u('cze\u015b\u0107')
        exc = ValueError(error_msg)

        result = force_bytes(exc)

        assert result == error_msg.encode('utf8')

    def test_date(self):
        date = datetime.date(2017, 9, 5)

        result = force_bytes(date)

        assert result == b'2017-09-05'

    def test_encoding(self):
        msg = u('cze\u015b\u0107')

        result = force_bytes(msg)

        assert result == b('cze\xc5\x9b\xc4\x87')

    def test_encoding_ignore(self):
        msg = u('cze\u015b\u0107')

        result = force_bytes(msg, encoding='ascii', errors='ignore')

        assert result == b('cze')


class TestGetVersion(object):

    @mock.patch('wykop.utils.get_distribution')
    def test_no_distribution(self, m_get_distribution):
        m_get_distribution.side_effect = DistributionNotFound

        result = get_version()

        assert result == 'dev'

    @mock.patch('wykop.utils.get_distribution')
    def test_version(self, m_get_distribution):
        class Distribution():
            def __init__(self, version):
                self.version = version

        version = mock.sentinel.version
        m_get_distribution.return_value = Distribution(version)

        result = get_version()

        assert result == version
