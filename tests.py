'''
Created on 22-12-2012

@author: artur.maciag
'''
import unittest
import os
from datetime import date

import wykop


class WykopAPITests(unittest.TestCase):

    def setUp(self):
        try:
            appkey = os.environ['APPKEY']
        except KeyError:
            self.fail("APPKEY not set")
        try:
            secretkey = os.environ['SECRETKEY']
        except KeyError:
            self.fail("SECRETKEY not set")
        self.api = wykop.WykopAPI(appkey, secretkey)
        self.api.login = os.environ['LOGIN']
        self.api.accountkey = os.environ['ACCOUNTKEY']

    def force_urllib2(self):
        import contextlib
        from urllib2 import Request, urlopen, HTTPError, URLError
        
        wykop.USE_REQUESTS = False
        wykop.contextlib = contextlib
        wykop.Request = Request
        wykop.urlopen = urlopen
        wykop.HTTPError = HTTPError
        wykop.URLError = URLError

    def test_get_link_success(self):
        self.api.get_link(1)

    def test_get_link_comments_success(self):
        self.api.get_link_comments(1)

    def test_get_link_reports_success(self):
        self.api.get_link_reports(1)

    def test_get_link_digs_success(self):
        self.api.get_link_digs(1)

    def test_get_link_related_success(self):
        self.api.get_link_related(1)

    def test_get_link_buryreasons_success(self):
        self.api.get_link_buryreasons()

    def test_get_links_promoted_success(self):
        self.api.get_links_promoted()

    def test_get_links_upcoming_success(self):
        self.api.get_links_upcoming()

    def test_get_popular_promoted_success(self):
        self.api.get_popular_promoted()

    def test_get_popular_upcoming_success(self):
        self.api.get_popular_upcoming()

    def test_get_top_success(self):
        self.api.get_top(date.today().year)

    def test_get_top_date_success(self):
        self.api.get_top_date(date.today().year, date.today().month)

    def test_get_entry_success(self):
        self.api.get_entry(1)

    def test_get_rank_success(self):
        self.api.get_rank()

    def test_get_observatory_votes_success(self):
        self.api.get_observatory_votes()

    def test_get_observatory_comments_success(self):
        self.api.get_observatory_comments()

    def test_get_observatory_entries_success(self):
        self.api.get_observatory_entries()

    def test_get_observatory_entries_comments_success(self):
        self.api.get_observatory_entries_comments()

    def test_add_entry_success(self):
        f = open('doge.png', 'rb')
        self.api.add_entry(body='#wykopsdk #wykopsdktest', embed=f)
        f.close()

if __name__ == '__main__':
    unittest.main()
