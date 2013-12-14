'''
Created on 18-12-2012

@author: maciag.artur
'''
import logging
import urlparse
import urllib
import urllib2
import hashlib
import contextlib
from datetime import date, timedelta
try: import simplejson as json
except ImportError: import json

__version__ = "0.1.1"

def paramsencode(d):
    return ','.join(['%s,%s' % (key, value) for (key, value) in d.items()])

def dictmap(d, f):
    return dict(map(lambda (k,v): (k, (v)), d.iteritems()))

def login_required(method):
    def decorator(self, *args, **kwargs):
        if not self.userkey:
            self.authenticate()
        try:
            return method(self, *args, **kwargs)
        # get new userkey on invalid key
        except InvalidUserKeyError:
            self.authenticate()
            return method(self, *args, **kwargs)
    return decorator

class AttrDict(dict): 
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

class WykopAPIError(Exception):
    def __init__(self, type_, message):
        Exception.__init__(self, message)
        self.type = type_

class InvalidAPIKeyError(WykopAPIError):
    pass

class InvalidParamsError(WykopAPIError):
    pass

class NotEnoughParamsError(WykopAPIError):
    pass

class AppWritePermissionsError(WykopAPIError):
    pass

class DailtyRequestLimitError(WykopAPIError):
    pass

class InvalidAPISignError(WykopAPIError):
    pass

class AppPermissionsError(WykopAPIError):
    pass

class InvalidUserKeyError(WykopAPIError):
    pass

class InvalidSessionKeyError(WykopAPIError):
    pass

class UserDoesNotExistError(WykopAPIError):
    pass

class InvalidCredentialsError(WykopAPIError):
    pass

class CredentialsMissingError(WykopAPIError):
    pass

class IPBannedError(WykopAPIError):
    pass

class UserBannedError(WykopAPIError):
    pass

class OwnVoteError(WykopAPIError):
    pass

class InvalidLinkIDError(WykopAPIError):
    pass

class OwnObserveError(WykopAPIError):
    pass

class CommentEditError(WykopAPIError):
    pass

class EntryEditError(WykopAPIError):
    pass

class RemovedLinkError(WykopAPIError):
    pass

class PrivateLinkError(WykopAPIError):
    pass

class EntryDoesNotExistError(WykopAPIError):
    pass

class QueryTooShortError(WykopAPIError):
    pass
    
class CommentDoesNotExistError(WykopAPIError):
    pass

class NiceTryError(WykopAPIError):
    pass

class UnreachableAPIError(WykopAPIError):
    pass

class NoIndexError(WykopAPIError):
    pass

__all_exceptions__ = {
    1:      InvalidAPIKeyError,
    2:      InvalidParamsError,
    3:      NotEnoughParamsError,
    4:      AppWritePermissionsError,
    5:      DailtyRequestLimitError,
    6:      InvalidAPISignError,
    7:      AppPermissionsError,
    11:     InvalidUserKeyError,
    12:     InvalidSessionKeyError,
    13:     UserDoesNotExistError,
    14:     InvalidCredentialsError,
    15:     CredentialsMissingError,
    17:     IPBannedError,
    18:     UserBannedError,
    31:     OwnVoteError,
    32:     InvalidLinkIDError,
    33:     OwnObserveError,
    34:     CommentEditError,
    35:     EntryEditError,
    41:     RemovedLinkError,
    42:     PrivateLinkError,
    61:     EntryDoesNotExistError,
    71:     QueryTooShortError,
    81:     CommentDoesNotExistError,
    999:    NiceTryError,
    1001:   UnreachableAPIError,
    1002:   NoIndexError
}

class WykopAPI:
    
    _protocol = 'http'
    _domain = "a.wykop.pl"
    
    def __init__(self, appkey, secretkey, login=None, accountkey=None, password=None):
        self.logger = logging.getLogger("wykop.WykopAPI")
        self.appkey = appkey
        self.secretkey = secretkey
        self.login = login
        self.accountkey = accountkey
        self.password = password
        self.userkey = ''
        if login and accountkey:
            self.authenticate()

    def _construct_url(self, rtype, rmethod, rmethod_params=[], api_params={}):
        # map all params to string
        rmethod_params = tuple(map(str, rmethod_params))
        # appkey is default for api_params
        api_params_all = {'appkey': self.appkey, 'userkey': self.userkey}
        api_params_all.update(api_params)
        api_params = paramsencode(api_params_all)
        
        pathparts = (rtype, rmethod) + rmethod_params + (api_params,)
        path = "/".join(pathparts)
        urlparts = (self._protocol, self._domain,  path, '', '', '')
        return str(urlparse.urlunparse(urlparts))

    def authenticate(self, login=None, accountkey=None, password=None):
        self.login = login or self.login
        self.accountkey = accountkey or self.accountkey
        self.password = password or self.password
        if not self.login or not (self.accountkey or self.password):
            raise WykopAPIError(0, "Login or (password or account key) not set")
        res = self.user_login(self.login, self.accountkey, self.password)
        self.userkey = res['userkey']

    def get_request_sign(self, url, post_params={}):
        post_values_list = [unicode(post_params[key]).encode('utf-8') for key in sorted(post_params.keys())]
        post_values = ",".join(post_values_list)
        return hashlib.md5(self.secretkey + url + post_values).hexdigest()

    def _request(self, url, data, sign):
        self.logger.debug(" Fetching url: `%s` (POST: %s, apisign: `%s`)" % 
                          (str(url), str(data), str(sign)))

        for key in data.keys():
            data[key] = unicode(data[key]).encode('utf-8')

        req = urllib2.Request(url, urllib.urlencode(data))
        req.add_header('User-Agent', "wykop-sdk/%s" % __version__)
        req.add_header('apisign', sign)
        
        try:
            with contextlib.closing(urllib2.urlopen(req)) as f:
                return f.read()
        except urllib2.HTTPError, e:
            raise WykopAPIError(0, str(e.code))
        except urllib2.URLError, e:
            raise WykopAPIError(0, str(e.reason))
        except Exception, e:
            raise WykopAPIError(0, 'Unhandled exception')

    def _parse_json(self, data):
        result = json.loads(data, object_hook=lambda x: AttrDict(x))
        if 'error' in result:
            exception_class = __all_exceptions__.get(result['error']['code'], WykopAPIError)
            raise exception_class(result['error']['code'], 
                                result['error']['message'])
        return result

    def request(self, rtype, rmethod, rmethod_params=[], 
                api_params={}, post_params={}, raw_response=False):
        self.logger.debug("Making request")
        post_params = dictmap(post_params, lambda x: x.encode('utf-8') if isinstance(x, unicode) else x)
        url = self._construct_url(rtype, rmethod, rmethod_params, api_params)
        apisign = self.get_request_sign(url, post_params)
        response = self._request(url, post_params, apisign)
        
        if raw_response:
            return response
        return self._parse_json(response)

    # Comments

    @login_required
    def add_comment(self, link_id, comment_id, body, embed=None):
        post_params = {'body': body}
        if embed:
            post_params.update({'embed': embed})
        return self.request('comments', 'add', [link_id, comment_id], 
                            post_params=post_params)

    @login_required
    def plus_comment(self, link_id, comment_id):
        return self.request('comments', 'plus', [link_id, comment_id])

    @login_required
    def minus_comment(self, link_id, comment_id):
        return self.request('comments', 'minus', [link_id, comment_id])

    @login_required
    def edit_comment(self, comment_id, body):
        post_params = {'body': body}
        return self.request('comments', 'edit', [comment_id],
                            post_params=post_params)

    @login_required
    def delete_comment(self, comment_id):
        return self.request('comments', 'delete', [comment_id])

    # Link

    def get_link(self, link_id):
        return self.request('link', 'index', [link_id])

    @login_required
    def dig_link(self, link_id):
        return self.request('link', 'dig', [link_id])

    @login_required
    def cancel_link(self, link_id):
        return self.request('link', 'cancel', [link_id])

    @login_required
    def bury_link(self, link_id, bury_id):
        return self.request('link', 'bury', [link_id, bury_id])

    def get_link_comments(self, link_id):
        return self.request('link', 'comments', [link_id])

    def get_link_reports(self, link_id):
        return self.request('link', 'reports', [link_id])

    def get_link_digs(self, link_id):
        return self.request('link', 'digs', [link_id])

    def get_link_related(self, link_id):
        return self.request('link', 'related', [link_id])

    def get_link_buryreasons(self):
        return self.request('link', 'buryreasons')

    @login_required
    def observe_link(self, link_id):
        return self.request('link', 'observe', [link_id])

    @login_required
    def favorite_link(self, link_id):
        return self.request('link', 'favorite', [link_id])

    # Links
    
    def get_links_promoted(self, page=1, sort='day'):
        api_params = {'appkey': self.appkey, 'page': page, 'sort': sort}
        return self.request('links', 'promoted',
                            api_params=api_params)

    def get_links_upcoming(self, page=1, sort='date'):
        api_params = {'appkey': self.appkey, 'page': page, 'sort': sort}
        return self.request('links', 'upcoming',
                            api_params=api_params)

    # Popular
    
    def get_popular_promoted(self):
        return self.request('popular', 'promoted',)

    def get_popular_upcoming(self):
        return self.request('popular', 'upcoming')

    # Profile

    def get_profile(self, username):
        return self.request('profile', 'index', [username])

    def get_profile_links(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'added', [username],
                            api_params=api_params)

    def get_profile_published(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'published', [username],
                            api_params=api_params)

    def get_profile_commented(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'commented', [username],
                            api_params=api_params)

    def get_profile_digged(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'digged', [username],
                            api_params=api_params)

    @login_required
    def get_profile_buried(self, username, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey, 'page': page}
        return self.request('profile', 'buried', [username],
                            api_params=api_params)

    @login_required
    def observe_profile(self, username):
        return self.request('profile', 'observe', [username])
    
    @login_required
    def unobserve_profile(self, username):
        return self.request('profile', 'unobserve', [username])

    def get_profile_followers(self, username, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey, 'page': page}
        return self.request('profile', 'followers', [username],
                            api_params=api_params)

    def get_profile_followed(self, username, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey, 'page': page}
        return self.request('profile', 'followed', [username],
                            api_params=api_params)

    def get_profile_favorites(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'favorites', [username],
                            api_params=api_params)

    # Search
    
    def search(self, q, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        post_params = {'q': q}
        return self.request('search', 'index',
                            api_params=api_params,
                            post_params=post_params)

    def search_links(self, q, page=1, what='all', sort='best', 
                     when='all', date_from=None, date_to=None, votes=0):
        date_from = date_to or (date.today() - timedelta(days=30) ).strftime("%d/%m/%Y")
        date_to = date_to or date.today().strftime("%d/%m/%Y")
        api_params = {'appkey': self.appkey, 'page': page}
        post_params = {'q': q, 'what': what, 'sort': sort, 'when': when,
                       'from': date_from, 'to': date_to, 'votes': votes}
        return self.request('search', 'links',
                            api_params=api_params,
                            post_params=post_params)

    def search_entries(self, q, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        post_params = {'q': q}
        return self.request('search', 'entries',
                            api_params=api_params,
                            post_params=post_params)

    def search_profiles(self, q):
        post_params = {'q': q}
        return self.request('search', 'entries',
                            post_params=post_params)

    # User

    def user_login(self, login, accountkey=None, password=None):
        post_params = {'login': login}

        if accountkey:
            post_params['accountkey'] = accountkey
        if password:
            post_params['password'] = password

        return self.request('user', 'login', 
                            post_params=post_params)

    @login_required
    def get_user_favorites(self):
        return self.request('user', 'favorites') 

    @login_required
    def get_user_observed(self):
        return self.request('user', 'observed') 

    # Top

    def get_top(self, year):
        return self.request('top', 'index', [year])

    def get_top_date(self, year, month, page=1):
        year = year or date.today().year
        post_params = {'page': page}
        return self.request('top', 'date', [year, month],
                            post_params=post_params)

    # Related

    @login_required
    def plus_related(self, link_id, related_id):
        return self.request('related', 'plus', [link_id, related_id])

    @login_required
    def minus_related(self, link_id, related_id):
        return self.request('related', 'minus', [link_id, related_id])

    @login_required
    def add_related(self, link_id, url, title):
        post_params = {'url': url, 'title': title}
        return self.request('related', 'add', [link_id],
                            post_params=post_params)

    # Entries

    def get_entry(self, entry_id):
        return self.request('entries', 'index', [entry_id])

    @login_required
    def add_entry(self, body, embed=None):
        post_params = {'body': body}
        if embed:
            post_params.update({'embed': embed})
        return self.request('entries', 'add', 
                            post_params=post_params)

    @login_required
    def edit_entry(self, entry_id, body):
        post_params = {'body': body}
        return self.request('entries', 'edit', 
                            post_params=post_params)

    @login_required
    def delete_entry(self, entry_id):
        return self.request('entries', 'delete', [entry_id])

    @login_required
    def add_entry_comment(self, entry_id, body, embed):
        post_params = {'body': body}
        if embed:
            post_params.update({'embed': embed})
        return self.request('entries', 'addcomment', [entry_id],
                            post_params=post_params)

    @login_required
    def edit_entry_comment(self, entry_id, comment_id, body):
        post_params = {'body': body}
        return self.request('entries', 'editcomment', [entry_id, comment_id],
                            post_params=post_params)

    @login_required
    def delete_entry_comment(self, entry_id, comment_id):
        return self.request('entries', 'deletecomment', [entry_id, comment_id])

    @login_required
    def vote_entry(self, entry_id):
        return self.request('entries', 'vote', ['entry', entry_id])

    @login_required
    def unvote_entry(self, entry_id):
        return self.request('entries', 'unvote', ['entry', entry_id])

    @login_required
    def vote_entry_comment(self, entry_id, comment_id):
        return self.request('entries', 'vote', ['comment', entry_id, comment_id])

    @login_required
    def unvote_entry_comment(self, entry_id, comment_id):
        return self.request('entries', 'unvote', ['comment', entry_id, comment_id])

    # Rank

    def get_rank(self):
        return self.request('rank', 'index')

    # Observatory

    def get_observatory_votes(self):
        return self.request('observatory', 'votes')

    def get_observatory_comments(self):
        return self.request('observatory', 'comments')

    def get_observatory_entries(self):
        return self.request('observatory', 'entries')

    def get_observatory_entries_comments(self):
        return self.request('observatory', 'entriescomments')

    # Favorites

    @login_required
    def get_favorites(self, list_id):
        return self.request('favorites', 'index', [list_id])

    @login_required
    def get_favorites_lists(self):
        return self.request('favorites', 'lists')

    # Stream
    
    def get_stream(self, page=1):
        return self.request('stream', 'index', [page])

    def get_stream_hot(self, page=1):
        return self.request('stream', 'hot', [page])

    # Tag

    def tag(self, tag_name, page=1):
        return self.request('tag', 'index',
                            [tag_name],
                            {'page': page})
    # PM

    @login_required
    def get_conversations_list(self):
        return self.request('pm', 'conversationslist')

    @login_required
    def get_conversation(self, username):
        return self.request('pm', 'conversation', [username])


    @login_required
    def send_message(self, username, body, embed=None):
        post_params = {'body': body}
        if embed:
            post_params.update({'embed': embed})
        return self.request('pm', 'sendmessage', [username],
                            post_params=post_params)

    @login_required
    def delete_conversation(self, username):
        return self.request('pm', 'deleteconversation', [username])
