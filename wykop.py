'''
Created on 18-12-2012

@author: maciag.artur
'''
import urlparse
import urllib
import urllib2
try: import simplejson as json
except ImportError: import json

def paramsencode(d):
    return ','.join(['%s,%s' % (key, value) for (key, value) in d.items()])

class WykopAPIError(Exception):
    def __init__(self, type, message):
        Exception.__init__(self, message)
        self.type = type

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
    
    def __init__(self, appkey, login=None, accountkey=None):
        self.appkey = appkey
        self.login = login
        self.accountkey = accountkey
        self.userkey = None

    def request(self, rtype, rmethod, rmethod_params=(), api_params={}, post_params={}):
        # map all params to string
        rmethod_params = tuple(map(str, rmethod_params))
        # appkey is default for api_params
        api_params = api_params or {'appkey': self.appkey}
        params = paramsencode(api_params)
        pathparts = (rtype, rmethod) + rmethod_params + (params,)
        path = "/".join(pathparts)
        urlparts = (self._protocol, self._domain,  path, '', '', '')
        url = urlparse.urlunparse(urlparts)
        
        try:
            f = urllib2.urlopen(url, urllib.urlencode(post_params))
        except urllib2.HTTPError, e:
            response = json.loads(e.read())
            raise WykopAPIError(response)
        
        try:
            response = json.loads(f.read())
            if 'error' in response:
                exception_class = __all_exceptions__.get(response['error']['code'], WykopAPIError)
                raise exception_class(response['error']['code'], 
                                    response['error']['message'])
        finally:
            f.close()
        return response

    def get_profile(self, username):
        return self.request('profile', 'index', (username,))

    def get_profile_links(self, username, page=1):
        return self.request('profile', 'added', (username, page))

    def user_login(self):
        params = {'login': self.login, 'accountkey': self.accountkey}
        return self.request('user', 'login', post_params=params)
