import base64
import hashlib
import logging
from datetime import date, timedelta

from six.moves.urllib.parse import urlunparse, quote_plus

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


class BaseWykopAPI(object):
    """
    Base Wykop API class
    """

    _client_name = 'wykop-sdk'
    _protocol = 'http'
    _domain = 'a.wykop.pl'

    def __init__(self, appkey, secretkey, login=None, accountkey=None,
                 password=None, output='', response_format='json'):
        self.appkey = appkey
        self.secretkey = secretkey
        self.login = login
        self.accountkey = accountkey
        self.password = password
        self.output = output
        self.format = response_format
        self.userkey = ''

    def get_method_params(self, *method_params):
        """
        Gets request method parameters.
        """
        # map all params to string
        return tuple(map(str, method_params))

    def get_default_api_params(self):
        """
        Gets default api parameters.
        """
        return {
            'appkey': self.appkey,
            'format': self.format,
            'output': self.output,
            'userkey': self.userkey,
        }

    def get_api_params(self, **api_params):
        """
        Gets request api parameters.
        """
        # default api params
        api_params_all = self.get_default_api_params()
        # update user defined api params
        api_params_all.update(api_params)
        # encode api params
        return paramsencode(api_params_all)

    def get_path(self, rtype, rmethod, *rmethod_params, **api_params):
        """
        Gets request path.
        """
        method_params = self.get_method_params(*rmethod_params)
        api_params = self.get_api_params(**api_params)

        pathparts = (rtype, rmethod) + method_params + (api_params,)
        return '/'.join(pathparts)

    def construct_url(self, rtype, rmethod, *rmethod_params, **api_params):
        """
        Constructs request url.
        """
        path = self.get_path(rtype, rmethod, *rmethod_params, **api_params)

        urlparts = (self._protocol, self._domain, path, '', '', '')
        return str(urlunparse(urlparts))

    def get_post_params_values(self, **post_params):
        """
        Gets post parameters values list. Required to api sign.
        """
        return [force_text(post_params[key])
                for key in sorted(post_params.keys())]

    def get_api_sign(self, url, **post_params):
        """
        Gets request api sign.
        """
        post_params_values = self.get_post_params_values(**post_params)
        post_params_values_str = ",".join(post_params_values)
        post_params_values_bytes = force_bytes(post_params_values_str)
        url_bytes = force_bytes(url)
        secretkey_bytes = force_bytes(self.secretkey)
        return hashlib.md5(
            secretkey_bytes + url_bytes + post_params_values_bytes).hexdigest()

    def get_user_agent(self):
        """
        Gets User-Agent header.
        """
        client_version = get_version()
        return '/'.join([self._client_name, client_version])

    def get_headers(self, url, **post_params):
        """
        Gets request headers.
        """
        apisign = self.get_api_sign(url, **post_params)
        user_agent = self.get_user_agent()

        return {
            'apisign': apisign,
            'User-Agent': user_agent,
        }

    def request(self, rtype, rmethod, rmethod_params=[],
                api_params={}, post_params={}, file_params={},
                parser=default_parser, requester=default_requester):
        """
        Makes request.
        """
        log.debug('Making request')

        # sanitize data
        rtype = force_text(rtype)
        rmethod = force_text(rmethod)
        post_params = dictmap(force_bytes, post_params)
        api_params = dictmap(force_text, api_params)

        url = self.construct_url(rtype, rmethod, *rmethod_params, **api_params)
        headers = self.get_headers(url, **post_params)

        response = requester.make_request(
            url, post_params, headers, file_params)

        if parser is None:
            return response

        return parser.parse(response)


class WykopAPI(BaseWykopAPI):
    """
    Wykop API class
    """

    def __init__(self, appkey, secretkey, login=None, accountkey=None,
                 password=None, output='', response_format='json'):
        super(WykopAPI, self).__init__(
            appkey, secretkey, login=login, accountkey=accountkey,
            password=password, output=output, response_format=response_format)

        if self.login and (self.accountkey or self.password):
            self.authenticate()

    def authenticate(self, login=None, accountkey=None, password=None):
        self.login = login or self.login
        self.accountkey = accountkey or self.accountkey
        self.password = password or self.password

        if not self.login or not (self.accountkey or self.password):
            raise WykopAPIError(
                0, 'Login or (password or account key) not set')

        res = self.user_login(self.login, self.accountkey, self.password)
        self.userkey = res['userkey']

    def user_login(self, login, accountkey=None, password=None):
        post_params = {'login': login}

        if accountkey:
            post_params['accountkey'] = accountkey
        if password:
            post_params['password'] = password

        return self.request('user', 'login', post_params=post_params)

    # Connect

    def get_connect_api_params(self, redirect_url):
        """
        Gets request api parameters for wykop connect.
        """
        redirect_url_encoded = quote_plus(base64.b64encode(redirect_url))
        apisign = self.get_api_sign(redirect_url)

        return {
            'redirect': redirect_url_encoded,
            'secure': apisign,
        }

    def get_connect_url(self, redirect_url):
        """
        Gets url for wykop connect.
        """
        api_params = self.get_connect_api_params(redirect_url)

        return self.construct_url('user', 'connect', **api_params)

    def get_connect_data(self, data, parser=default_parser):
        """
        Gets decoded data from wykop connect.
        """
        decoded = base64.decodestring(data)
        parsed = parser.parse(decoded)
        return parsed['appkey'], parsed['login'], parsed['token']

    # Comments

    @login_required
    def add_comment(self, link_id, comment_id, body, embed=None):
        post_params = {'body': body}
        file_params = {}

        if embed:
            if hasattr(embed, 'read'):
                file_params.update({'embed': embed})
            else:
                post_params.update({'embed': embed})

        return self.request('comments', 'add', [link_id, comment_id],
                            post_params=post_params,
                            file_params=file_params)

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

    # MyWykop

    @login_required
    def get_mywykop(self, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey,
                      'page': page}
        return self.request('mywykop', 'index',
                            api_params=api_params)

    @login_required
    def get_mywykop_tags(self, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey,
                      'page': page}
        return self.request('mywykop', 'tags',
                            api_params=api_params)

    @login_required
    def get_mywykop_users(self, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey,
                      'page': page}
        return self.request('mywykop', 'users',
                            api_params=api_params)

    @login_required
    def get_notifications(self, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey,
                      'page': page}
        return self.request('mywykop', 'notifications',
                            api_params=api_params)

    @login_required
    def get_notifications_count(self):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey}
        return self.request('mywykop', 'notificationscount',
                            api_params=api_params)

    @login_required
    def get_hashtags_notifications(self, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey,
                      'page': page}
        return self.request('mywykop', 'hashtagsnotifications',
                            api_params=api_params)

    @login_required
    def get_hashtags_notifications_count(self):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey}
        return self.request('mywykop', 'hashtagsnotificationscount',
                            api_params=api_params)

    @login_required
    def mark_as_read_notifications(self):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey}
        return self.request('mywykop', 'readnotifications',
                            api_params=api_params)

    @login_required
    def mark_as_read_hashtags_notifications(self):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey}
        return self.request('mywykop', 'readhashtagsnotifications',
                            api_params=api_params)

    @login_required
    def mark_as_read_notification(self, notification_id):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey}
        return self.request('mywykop', 'markasreadnotification',
                            [notification_id],
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

    def get_profile_comments(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'comments', [username],
                            api_params=api_params)

    def get_profile_digged(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'digged', [username],
                            api_params=api_params)

    @login_required
    def get_profile_buried(self, username, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey,
                      'page': page}
        return self.request('profile', 'buried', [username],
                            api_params=api_params)

    @login_required
    def observe_profile(self, username):
        return self.request('profile', 'observe', [username])

    @login_required
    def unobserve_profile(self, username):
        return self.request('profile', 'unobserve', [username])

    @login_required
    def block_profile(self, username):
        return self.request('profile', 'block', [username])

    @login_required
    def unblock_profile(self, username):
        return self.request('profile', 'unblock', [username])

    def get_profile_followers(self, username, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey,
                      'page': page}
        return self.request('profile', 'followers', [username],
                            api_params=api_params)

    def get_profile_followed(self, username, page=1):
        api_params = {'appkey': self.appkey, 'userkey': self.userkey,
                      'page': page}
        return self.request('profile', 'followed', [username],
                            api_params=api_params)

    def get_profile_favorites(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'favorites', [username],
                            api_params=api_params)

    def get_profile_entries(self, username, page=1):
        api_params = {'appkey': self.appkey, 'page': page}
        return self.request('profile', 'entries', [username],
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
        date_from = date_to or (date.today() - timedelta(days=30))
        date_from_str = date_from.strftime("%d/%m/%Y")
        date_to = date_to or date.today().strftime("%d/%m/%Y")
        api_params = {'appkey': self.appkey, 'page': page}
        post_params = {'q': q, 'what': what, 'sort': sort, 'when': when,
                       'from': date_from_str, 'to': date_to, 'votes': votes}
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
    def add_entry(self, body, embed=None, channel=None):
        post_params = {'body': body}
        file_params = {}

        if embed:
            if hasattr(embed, 'read'):
                file_params.update({'embed': embed})
            else:
                post_params.update({'embed': embed})
        if channel:
            post_params.update({'channel': channel})

        return self.request('entries', 'add',
                            post_params=post_params,
                            file_params=file_params)

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
        return self.request('entries', 'vote', ['comment', entry_id,
                                                comment_id])

    @login_required
    def unvote_entry_comment(self, entry_id, comment_id):
        return self.request('entries', 'unvote', ['comment', entry_id,
                                                  comment_id])

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
        file_params = {}

        if embed:
            if hasattr(embed, 'read'):
                file_params.update({'embed': embed})
            else:
                post_params.update({'embed': embed})

        return self.request('pm', 'sendmessage', [username],
                            post_params=post_params,
                            file_params=file_params)

    @login_required
    def delete_conversation(self, username):
        return self.request('pm', 'deleteconversation', [username])
