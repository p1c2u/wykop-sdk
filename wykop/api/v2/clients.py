import base64
import logging
from collections import OrderedDict

from six.moves.urllib.parse import urlunparse, quote_plus

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
        params = self.get_default_api_params()
        params.update(api_params)
        # sort
        params_ordered = OrderedDict(sorted(params.items()))
        # map all params to string
        for key, value in params_ordered.items():
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

    # Addlink

    @login_required
    def add_link_draft(self, url):
        """
        Przygotowanie szkicu nowego znaleziska.

        :param url: adres URL
        :type url: str
        """
        raise NotImplementedError

    @login_required
    def get_link_draft_images(self, key):
        """
        Pobranie obrazków szkicu nowego znaleziska.

        :param key: klucz szkicu
        :type key: str
        """
        raise NotImplementedError

    @login_required
    def add_link(self, key, url, title, description, tags, plus18=False):
        """
        Dodanie nowego znaleziska.

        :param key: klucz szkicu
        :param url: adres URL
        :param title: tytuł
        :param description: opis
        :param tags: tagi
        :param plus18: oznaczenie +18
        :type key: str
        :type url: str
        :type title: str
        :type description: str
        :type tags: str
        :type plus18: bool
        """
        raise NotImplementedError

    # Connect

    def get_connect_url(self, redirect_url=None):
        """
        Gets url for wykop connect.
        """
        api_params = self.get_connect_api_params(redirect_url)

        return self.construct_url('login', 'connect', **api_params)

    # entries

    def get_stream_entries(self, page=1, firstid=None):
        """Pobranie listy wpisów.
        
        :param page: numer strony
        :param firstid: id pierwszego wpisu na liście
        :type page: int
        :type firstid: int
        """
        api_params = {
            'page': page,
        }
        return self.request('entries', 'stream', api_params=api_params)

    def get_hot_entries(self, period=12, page=1):
        """Pobranie listy Gorących wpisów.
        
        :param period: okres w liczbie miesięcy (6, 12 lub 24)
        :param page: numer strony
        :type period: int
        :type page: int
        """
        assert period in [6, 12, 24]
        api_params = {
            'period': period,
            'page': page,
        }
        return self.request('entries', 'hot', api_params=api_params)

    def get_active_entries(self, page=1):
        """Pobranie listy Aktywnych wpisów.
        
        :param page: numer strony
        :type page: int
        """
        raise NotImplementedError

    @login_required
    def get_observed_entries(self, page=1):
        """Pobranie listy Obserwowanych wpisów.
        
        :param page: numer strony
        :type page: int
        """
        raise NotImplementedError

    def get_entry(self, entry_id):
        """Pobranie pojedyńczego wpisu.
        
        :param entry_id: id wpisu
        :type entry_id: int
        """
        api_params = {
            'entry': entry_id,
        }
        return self.request('entries', api_params=api_params)

    @login_required
    def add_entry(self, body, embed=None):
        """Dodanie nowego wpisu.
        
        :param body: treść
        :param embed: załącznik w formie obrazka lub linku
        :type body: str
        :type embed: file, str
        """
        raise NotImplementedError

    @login_required
    def edit_entry(self, entry_id, body, embed=None):
        """Edycja wpisu.
        
        :param entry_id: id wpisu
        :param body: treść
        :param embed: załącznik w formie obrazka lub linku
        :type entry_id: int
        :type body: str
        :type embed: file, str
        """
        raise NotImplementedError

    @login_required
    def vote_up_entry(self, entry_id):
        """Plusowanie wpisu.
        
        :param entry_id: id wpisu
        :type entry_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_remove_entry(self, entry_id):
        """Zgłoszenie wpisu.
        
        :param entry_id: id wpisu
        :type entry_id: int
        """
        raise NotImplementedError

    @login_required
    def delete_entry(self, entry_id):
        """Usunięcie wpisu.
        
        :param entry_id: id wpisu
        :type entry_id: int
        """
        raise NotImplementedError

    def get_entry_comment(self, entry_comment_id):
        """Pobranie pojedyńczego komentarza do wpisu.
        
        :param entry_comment_id: id wpisu
        :type entry_comment_id: int
        """
        raise NotImplementedError

    @login_required
    def add_entry_comment(self, entry_id, body, embed=None):
        """Dodanie nowego komentarza do wpisu.
        
        :param entry_id: id wpisu
        :param body: treść
        :param embed: załącznik w formie obrazka lub linku
        :type entry_id: int
        :type body: str
        :type embed: file, str
        """
        raise NotImplementedError

    @login_required
    def edit_entry_comment(self, body, embed=None):
        """Edycja komentarza do wpisu.
        
        :param body: treść
        :param embed: załącznik w formie obrazka lub linku
        :type body: str
        :type embed: file, str
        """
        raise NotImplementedError

    @login_required
    def delete_entry_comment(self, entry_comment_id):
        """Usunięcie komentarza do wpisu.
        
        :param entry_comment_id: id wpisu
        :type entry_comment_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_up_entry_comment(self, entry_comment_id):
        """Plusowanie komentarza do wpisu.
        
        :param entry_comment_id: id wpisu
        :type entry_comment_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_remove_entry_comment(self, entry_comment_id):
        """Zgłoszenie komentarza do wpisu.
        
        :param entry_comment_id: id wpisu
        :type entry_comment_id: int
        """
        raise NotImplementedError

    @login_required
    def set_favorite_entry(self, entry_id):
        """Oznaczenie/odznaczenie wpisu jako ulubiony.
        
        :param entry_id: id wpisu
        :type entry_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_survey_entry(self, entry_id, survey_id):
        """Zagłosowanie w ankiecie do wpisu.
        
        :param entry_id: id wpisu
        :param survey_id: id ankiety
        :type entry_id: int
        :type survey_id: int
        """
        raise NotImplementedError

    # hits

    def get_hits_popular(self):
        """Pobranie listy popularnych znalezisk."""
        return self.request('hits', 'popular')

    def get_hits_day(self):
        """Pobranie listy najlepszych znalezisk dnia."""
        return self.request('hits', 'day')

    def get_hits_week(self):
        """Pobranie listy najlepszych znalezisk tygodnia."""
        return self.request('hits', 'week')

    def get_hits_month(self, year=None, month=None, page=1):
        """Pobranie listy najlepszych znalezisk miesiąca.
        
        :param year: rok (domyślnie aktualny)
        :param month: miesiąc (domyślnie aktualny)
        :param page: strona
        :type year: int
        :type month: int
        :type page: int
        """
        api_params = {}

        if year and month:
            api_params.update({
                str(year): month,
            })

        if page:
            api_params.update({
                'page': page,
            })
        return self.request('hits', 'month', api_params=api_params)

    def get_hits_year(self, year=None):
        """Pobranie listy najlepszych znalezisk roku.
        
        :param year: rok (domyślnie aktualny)
        :type year: int
        """
        api_params = {}

        if year and month:
            api_params.update({
                str(year): month,
            })

        return self.request('hits', 'week', api_params=api_params)

    # links

    def get_links_promoted(self, page=1):
        """Pobranie listy promowanych znalezisk.
        
        :param page: strona
        :type page: int
        """
        api_params = {
            'page': page,
        }
        return self.request('links', 'promoted', api_params=api_params)

    def get_links_upcoming(self, sort='active', page=1):
        """Pobranie listy znalezisk z wykopaliska.
        
        :param sort: sortowanie (active, date, votes lub comments)
        :param page: strona
        :type sort: str
        :type page: int
        """
        assert sort in ['active', 'date', 'votes', 'comments']
        api_params = {
            'sort': sort,
            'page': page,
        }
        return self.request('links', 'upcoming', api_params=api_params)

    @login_required
    def get_links_observed(self, page=1):
        """Pobranie obserwowanych znalezisk z wszystkich list.
        
        :param page: strona
        :type page: int
        """
        api_params = {
            'page': page,
        }
        return self.request('links', 'observed', api_params=api_params)

    def get_link(self, link_id, with_comments=False):
        """Pobranie pojedyńczego znaleziska.
        
        :param link_id: id znaleziska
        :param with_comments: pobranie listy komentarzy ze znaleziskiem
        :type link_id: int
        :type with_comments: bool
        """
        api_params = {
            'id': link_id,
        }
        return self.request('links', 'link', api_params=api_params)

    @login_required
    def vote_up_link(self, link_id):
        """Wykopanie znaleziska.
        
        :param link_id: id znaleziska
        :type link_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_remove_link(self, link_id):
        """Zgłoszenie znaleziska.
        
        :param link_id: id znaleziska
        :type link_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_down_link(self, link_id, vote_type):
        """Zakopanie znaleziska.
        
        :param link_id: id znaleziska
        :param vote_type: powód zakopania (1-duplikat, 2-spam, 3-informacja nieprawdziwa, 4-treść nieodpowiednia, 5-nie nadaje się)
        :type link_id: int
        :type vote_type: int
        """
        raise NotImplementedError

    def get_link_upvoters(self, link_id):
        """Pobranie listy wykopujących.
        
        :param link_id: id znaleziska
        :type link_id: int
        """
        api_params = {
            'upvoters': link_id,
        }
        return self.request('links', api_params=api_params)

    def get_link_downvoters(self, link_id):
        """Pobranie listy zakopujących.
        
        :param link_id: id znaleziska
        :type link_id: int
        """
        api_params = {
            'downvoters': link_id,
        }
        return self.request('links', api_params=api_params)

    def get_top_links(self, year, month=None):
        """Pobranie listy najlepszych znalezisk.
        
        :param year: rok
        :param month: miesiąc
        :type year: int
        :type month: int
        """
        api_params = {
            'year': year,
        }

        if month:
            api_params.update({
                'month': month,
            })
        return self.request('links', 'top', api_params=api_params)

    def get_link_comments(self, link_id, sort='old'):
        """Pobranie listy komentarzy do znaleziska.
        
        :param link_id: id znaleziska
        :param sort: sortowanie (old, new lub best)
        :type link_id: int
        :type sort: str
        """
        assert sort in ['old', 'new', 'best']
        api_params = {
            'comments': link_id,
            'sort': sort,
        }
        return self.request('links', api_params=api_params)

    @login_required
    def vote_up_link_comment(self, link_id, comment_id):
        """Plusowanie komentarza do znaleziska.
        
        :param link_id: id znaleziska
        :param comment_id: id komentarza
        :type link_id: int
        :type comment_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_down_link_comment(self, link_id, comment_id):
        """Minusowanie komentarza do znaleziska.
        
        :param link_id: id znaleziska
        :param comment_id: id komentarza
        :type link_id: int
        :type comment_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_cancel_link_comment(self, link_id, comment_id):
        """Cofnięcie plusa/minusa komentarza do znaleziska.
        
        :param link_id: id znaleziska
        :param comment_id: id komentarza
        :type link_id: int
        :type comment_id: int
        """
        raise NotImplementedError

    @login_required
    def add_link_comment(self, link_id, body, embed=None, comment_id=None):
        """Dodanie komentarza do znaleziska.
        
        :param link_id: id znaleziska
        :param body: treść
        :param embed: załącznik w formie obrazka lub linku
        :param comment_id: id komentarza (jeżeli odpowiedź do komentarza)
        :type link_id: int
        :type body: str
        :type embed: file, str
        :type comment_id: int
        """
        raise NotImplementedError

    @login_required
    def edit_link_comment(self, comment_id, body, embed=None):
        """Edycja komentarza do znaleziska.
        
        :param comment_id: id komentarza
        :param body: treść
        :param embed: załącznik w formie obrazka lub linku
        :type comment_id: int
        :type body: str
        :type embed: file, str
        """
        raise NotImplementedError

    def get_link_comment(self, comment_id):
        """Pobranie pojedyńczego komentarza do znaleziska.
        
        :param comment_id: id komentarza
        :type comment_id: int
        """
        raise NotImplementedError

    def get_link_related(self, link_id):
        """Pobranie listy powiązanych do znaleziska.
        
        :param link_id: id znaleziska
        :type link_id: int
        """
        api_params = {
            'related': link_id,
        }
        return self.request('links', api_params=api_params)

    @login_required
    def vote_up_link_related(self, link_id, related_link_id):
        """Plusowanie powiązanego linku do znaleziska.
        
        :param link_id: id znaleziska
        :param related_link_id: id powiązanego linku do znaleziska
        :type link_id: int
        :type related_link_id: int
        """
        raise NotImplementedError

    @login_required
    def vote_down_link_related(self, link_id, related_link_id):
        """Minusowanie powiązanego linku do znaleziska.
        
        :param link_id: id znaleziska
        :param related_link_id: id powiązanego linku do znaleziska
        :type link_id: int
        :type related_link_id: int
        """
        raise NotImplementedError

    @login_required
    def set_favorite_link(self, link_id):
        """Oznaczenie/odznaczenie znaleziska jako ulubiony.
        
        :param link_id: id znaleziska
        :type link_id: int
        """
        raise NotImplementedError

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
