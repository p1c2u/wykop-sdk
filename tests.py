'''
Created on 22-12-2012

@author: artur.maciag
'''
import unittest
import os
from datetime import date

from wykop import WykopAPI

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
        self.api = WykopAPI(appkey, secretkey)
        self.api.login = os.environ['LOGIN']
        self.api.accountkey = os.environ['ACCOUNTKEY']

    def test_get_link_success(self):
        self.api.get_link(1)
        
        self.assert_(True)

    def test_get_link_comments_success(self):
        self.api.get_link_comments(1)
        
        self.assert_(True)

    def test_get_link_reports_success(self):
        self.api.get_link_reports(1)
        
        self.assert_(True)

    def test_get_link_digs_success(self):
        self.api.get_link_digs(1)
        
        self.assert_(True)

    def test_get_link_related_success(self):
        self.api.get_link_related(1)
        
        self.assert_(True)

    def test_get_link_buryreasons_success(self):
        self.api.get_link_buryreasons()
        
        self.assert_(True)

    def test_get_links_promoted_success(self):
        self.api.get_links_promoted()
        
        self.assert_(True)

    def test_get_links_upcoming_success(self):
        self.api.get_links_upcoming()
        
        self.assert_(True)

    def test_get_popular_promoted_success(self):
        self.api.get_popular_promoted()
        
        self.assert_(True)

    def test_get_popular_upcoming_success(self):
        self.api.get_popular_upcoming()
        
        self.assert_(True)

    def test_get_top_success(self):
        self.api.get_top(date.today().year)
        
        self.assert_(True)

    def test_get_top_date_success(self):
        self.api.get_top_date(date.today().year, date.today().month)
        
        self.assert_(True)

    def test_get_entry_success(self):
        self.api.get_entry(1)
        
        self.assert_(True)

    def test_get_rank_success(self):
        self.api.get_rank()
        
        self.assert_(True)

    def test_get_observatory_votes_success(self):
        self.api.get_observatory_votes()
        
        self.assert_(True)

    def test_get_observatory_comments_success(self):
        self.api.get_observatory_comments()
        
        self.assert_(True)

    def test_get_observatory_entries_success(self):
        self.api.get_observatory_entries()
        
        self.assert_(True)

    def test_get_observatory_entries_comments_success(self):
        self.api.get_observatory_entries_comments()
        
        self.assert_(True)

    def test_add_entry_success(self):
        self.api.add_entry(body='#wykopsdk #wykopsdktest', embed=open('doge.png', 'rb'))
        
        self.assert_(True)

if __name__ == '__main__':
    unittest.main()
