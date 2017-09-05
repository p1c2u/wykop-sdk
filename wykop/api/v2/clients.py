import logging
from collections import OrderedDict

from six.moves.urllib.parse import urlunparse

from wykop.api.clients import BaseWykopAPI
from wykop.api.decorators import login_required
from wykop.api.exceptions import WykopAPIError
from wykop.api.parsers import default_parser
from wykop.api.requesters import default_requester
from wykop.utils import (
    dictmap,
    paramsencode,
    force_bytes,
    force_text,
    get_version,
)

log = logging.getLogger(__name__)


class BaseWykopAPIv2(BaseWykopAPI):
    """Base Wykop API version 2."""

    _protocol = 'https'
    _domain = 'a2.wykop.pl'

    def request(self, rtype, rmethod=None,
                api_params=None, post_params=None, file_params=None,
                parser=default_parser, requester=default_requester):
        """
        Makes request.
        """
        log.debug('Making request')

        api_params = api_params or {}
        post_params = post_params or {}
        file_params = file_params or {}

        # sanitize data
        rtype = force_text(rtype)
        rmethod = rmethod and force_text(rmethod)
        post_params = dictmap(force_bytes, post_params)
        api_params = dictmap(force_text, api_params)

        url = self.construct_url(rtype, rmethod, **api_params)
        headers = self.get_headers(url, **post_params)

        response = requester.make_request(
            url, post_params, headers, file_params)

        if parser is None:
            return response

        return parser.parse(response)

    def construct_url(self, rtype, rmethod=None, **api_params):
        """
        Constructs request url.
        """
        path = self.get_path(rtype, rmethod=rmethod, **api_params)

        urlparts = (self._protocol, self._domain, path, '', '', '')
        return str(urlunparse(urlparts))

    def get_path(self, rtype, rmethod=None, **api_params):
        """
        Gets request path.
        """
        pathparts = (rtype, )

        if rmethod is not None:
            pathparts += (rmethod, )

        api_params = self.get_api_params(**api_params)

        if api_params:
            pathparts += tuple(api_params)

        return '/'.join(pathparts)

    def get_api_params(self, **api_params):
        """
        Gets request method parameters.
        """
        default_params = self.get_default_api_params()
        # sort
        params = OrderedDict(api_params)
        params.update([
            (k, default_params[k])
            for k in sorted(default_params, key=default_params.get)
        ])
        # map all params to string
        for key, value in params.items():
            if not value:
                continue
            yield str(key)
            yield str(value)


class WykopAPIv2(BaseWykopAPIv2):
    """Wykop API version 2."""

    appkey = 'aNd401dAPp'

    def authenticate(self, login=None, accountkey=None, password=None):
        self.login = login or self.login
        self.accountkey = accountkey or self.accountkey
        self.password = password or self.password

        if not self.login or not (self.accountkey or self.password):
            raise WykopAPIError(
                0, 'Login or (password or account key) not set')

        res = self.user_login(self.login, self.accountkey, self.password)
        self.userkey = res['data']['userkey']

    def user_login(self, login, accountkey=None, password=None):
        post_params = {
            'login': login,
        }

        if accountkey:
            post_params['accountkey'] = accountkey
        if password:
            post_params['password'] = password

        return self.request('login', post_params=post_params)

    # entries

    def get_entry(self, entry_id):
        api_params = {
            'entry': entry_id,
        }
        return self.request('entries', api_params=api_params)

    def get_stream_entries(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('entries', 'stream', api_params=api_params)

    def get_hot_entries(self, period=12, page=1):
        assert period in [6, 12, 24]
        api_params = {
            'period': period,
            'page': page,
        }
        return self.request('entries', 'hot', api_params=api_params)

    # links

    def get_links_promoted(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('links', 'promoted', api_params=api_params)

    def get_links_upcoming(self, sort='active', page=1):
        assert sort in ['active', 'date', 'votes', 'comments']
        api_params = {
            'sort': sort,
            'page': page,
        }
        return self.request('links', 'upcoming', api_params=api_params)

    def get_link_comments(self, link_id, sort='old'):
        assert sort in ['old', 'new', 'best']
        api_params = {
            'comments': link_id,
            'sort': sort,
        }
        return self.request('links', api_params=api_params)

    def get_link_related(self, link_id):
        api_params = {
            'related': link_id,
        }
        return self.request('links', api_params=api_params)

    def get_link_upvoters(self, link_id):
        api_params = {
            'upvoters': link_id,
        }
        return self.request('links', api_params=api_params)

    def get_link_downvoters(self, link_id):
        api_params = {
            'downvoters': link_id,
        }
        return self.request('links', api_params=api_params)

    # mywykop

    @login_required
    def get_mywykop(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('mywykop', api_params=api_params)

    @login_required
    def get_mywykop_tags(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('mywykop', 'tags', api_params=api_params)

    @login_required
    def get_mywykop_users(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('mywykop', 'users', api_params=api_params)

    @login_required
    def get_moj(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('moj', api_params=api_params)

    @login_required
    def get_moj_tagi(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('moj', 'tagi', api_params=api_params)

    # profiles

    def get_profile(self, username):
        return self.request('profiles', username)

    @login_required
    def observe_profile(self, username):
        api_params = {
            'observe': username,
        }
        return self.request('profiles', api_params=api_params)

    @login_required
    def unobserve_profile(self, username):
        api_params = {
            'unobserve': username,
        }
        return self.request('profiles', api_params=api_params)

    @login_required
    def block_profile(self, username):
        api_params = {
            'block': username,
        }
        return self.request('profiles', api_params=api_params)

    @login_required
    def unblock_profile(self, username):
        api_params = {
            'unblock': username,
        }
        return self.request('profiles', api_params=api_params)

    # hits

    def get_hits_month(self, year, month, page=1):
        api_params = {
            str(year): month,
            'page': page,
        }
        return self.request('hits', 'month', api_params=api_params)

    def get_hits_popular(self):
        return self.request('hits', 'popular')

    # pm

    @login_required
    def get_conversations_list(self):
        return self.request('pm', 'conversationsList')

    # notifications

    def get_notifications(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('notifications', api_params=api_params)

    def get_hashtags_notifications(self, page=1):
        api_params = {
            'page': page,
        }
        return self.request('notifications', 'hashtags', api_params=api_params)

    @login_required
    def get_notifications_count(self):
        return self.request('notifications', 'totalcount')

    def get_hashtags_notifications_count(self):
        return self.request('notifications', 'hashtagscount')

    # search

    def search_entries(self, query, page=1):
        post_params = {
            'q': query,
            'page': page,
        }
        return self.request('search', 'entries', post_params=post_params)

    def search_links(self, query, page=1):
        post_params = {
            'q': query,
            'page': page,
        }
        return self.request('search', 'links', post_params=post_params)

    def search_profiles(self, query):
        post_params = {
            'q': query,
        }
        return self.request('search', 'profiles', post_params=post_params)

    # tags

    def get_tag(self, name, page=1):
        api_params = {
            'page': page,
        }
        return self.request('tags', name, api_params=api_params)

    @login_required
    def get_tags_observed(self):
        return self.request('tags', 'observed')

    def get_tag_entries(self, name, page=1):
        api_params = {
            'entries': name,
            'page': page,
        }
        return self.request('tags', api_params=api_params)

    def get_tag_links(self, name, page=1):
        api_params = {
            'links': name,
            'page': page,
        }
        return self.request('tags', api_params=api_params)

    # tagi

    def get_tagi(self, name, page=1):
        api_params = {
            'page': page,
        }
        return self.request('tags', name, api_params=api_params)
