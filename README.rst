Wykop API Python SDK
====================

.. role:: strike
    :class: strike

.. image:: https://badge.fury.io/py/wykop-sdk.png
    :target: http://badge.fury.io/py/wykop-sdk

.. image:: https://travis-ci.org/p1c2u/wykop-sdk.svg?branch=master
    :target: https://travis-ci.org/p1c2u/wykop-sdk

.. image:: https://img.shields.io/codecov/c/github/p1c2u/wykop-sdk/master.svg?style=flat
    :target: https://codecov.io/github/p1c2u/wykop-sdk?branch=master

Biblioteka ta jest implementacją `Wykop API`_ w Python.

.. _Wykop API: http://www.wykop.pl/developers/api/

Przykładowe użycie:

::

    import wykop

    api = wykop.WykopAPI(klucz_aplikacji, sekret_aplikacji)
    profile = api.get_profile("m__b")

Instalacja
-------------------

Zalecana jest instalacja wykop-sdk poprzez pip:

::

    $ pip install wykop-sdk

Alternatywnie możesz pobrać kod i zainstalować bezpośrednio z repozytorium:

::

    $ pip install -e git+https://github.com/p1c2u/wykop-sdk.git#egg=wykop-sdk

Uwierzytelnienie
-------------------

Aby wykonywać działania jako użytkownik zalogowany przed wykonaniem metody należy się uwierzytenić.

Przykładowe użycie metody wymagającej uwierzytelnienia:

::

    import wykop

    api = wykop.WykopAPI(klucz_aplikacji, sekret_aplikacji)
    api.authenticate(login, klucz_polaczenia)
    profile = api.observe_profile("m__b")

API wersja 1
-------------------

Zdefiniowane metody
^^^^^^^^^^^^^^^^^^^

Biblioteka posiada wbudowane metody odpowiednie do zdefiniowanych w Wykop API

+-------------------+--------------------------------+
| Metoda API        | Metoda SDK                     |
+===================+================================+
| **Comments**                                       |
+-------------------+--------------------------------+
| Add               | add_comment                    |
+-------------------+--------------------------------+
| Plus              | plus_comment                   |
+-------------------+--------------------------------+
| Minus             | minus_comment                  |
+-------------------+--------------------------------+
| Edit              | edit_comment                   |
+-------------------+--------------------------------+
| Delete            | delete_comment                 |
+-------------------+--------------------------------+
| **Link**                                           |
+-------------------+--------------------------------+
| Index             | get_link                       |
+-------------------+--------------------------------+
| Dig               | dig_link                       |
+-------------------+--------------------------------+
| Cancel            | cancel_link                    |
+-------------------+--------------------------------+
| Bury              | bury_link                      |
+-------------------+--------------------------------+
| Comments          | get_link_comments              |
+-------------------+--------------------------------+
| Reports           | get_link_reports               |
+-------------------+--------------------------------+
| Digs              | get_link_digs                  |
+-------------------+--------------------------------+
| Related           | get_link_related               |
+-------------------+--------------------------------+
| Buryreasons       | get_link_buryreasons           |
+-------------------+--------------------------------+
| Observe           | observe_link                   |
+-------------------+--------------------------------+
| Favorite          | favorite_link                  |
+-------------------+--------------------------------+
| **Links**                                          |
+-------------------+--------------------------------+
| Promoted          | get_links_promoted             |
+-------------------+--------------------------------+
| Upcoming          | get_links_upcoming             |
+-------------------+--------------------------------+
| **MyWykop**                                        |
+-------------------+--------------------------------+
| Index             | get_mywykop                    |
+-------------------+--------------------------------+
| Tags              | get_mywykop_tags               |
+-------------------+--------------------------------+
| Users             | get_mywykop_users              |
+-------------------+--------------------------------+
| Notifications     | get_notifications              |
+-------------------+--------------------------------+
| NotificationsCount| get_notifications_count        |
+-------------------+--------------------------------+
| ReadNotifications | mark_as_read_notifications     |
+-------------------+--------------------------------+
| **Popular**                                        |
+-------------------+--------------------------------+
| Promoted          | get_popular_promoted           |
+-------------------+--------------------------------+
| Upcoming          | get_popular_upcoming           |
+-------------------+--------------------------------+
| **Profile**                                        |
+-------------------+--------------------------------+
| Index             | get_profile                    |
+-------------------+--------------------------------+
| Added             | get_profile_links              |
+-------------------+--------------------------------+
| Published         | get_profile_published          |
+-------------------+--------------------------------+
| Commented         | get_profile_commented          |
+-------------------+--------------------------------+
| Digged            | get_profile_digged             |
+-------------------+--------------------------------+
| Buried            | get_profile_buried             |
+-------------------+--------------------------------+
| Observe           | observe_profile                |
+-------------------+--------------------------------+
| Unobserve         | unobserve_profile              |
+-------------------+--------------------------------+
| Followers         | get_profile_followers          |
+-------------------+--------------------------------+
| Followed          | get_profile_followed           |
+-------------------+--------------------------------+
| Favorites         | get_profile_favorites          |
+-------------------+--------------------------------+
| **Search**                                         |
+-------------------+--------------------------------+
| Index             | search                         |
+-------------------+--------------------------------+
| Links             | search_links                   |
+-------------------+--------------------------------+
| Entries           | search_entries                 |
+-------------------+--------------------------------+
| Profiles          | search_profiles                |
+-------------------+--------------------------------+
| **User**                                           |
+-------------------+--------------------------------+
| Login             | user_login                     |
+-------------------+--------------------------------+
| Favorites         | user_favorites                 |
+-------------------+--------------------------------+
| Observed          | user_observed                  |
+-------------------+--------------------------------+
| **Top**                                            |
+-------------------+--------------------------------+
| Index             | get_top                        |
+-------------------+--------------------------------+
| Date              | get_top_date                   |
+-------------------+--------------------------------+
| **Related**                                        |
+-------------------+--------------------------------+
| Plus              | plus_related                   |
+-------------------+--------------------------------+
| Minus             | minus_related                  |
+-------------------+--------------------------------+
| Add               | add_related                    |
+-------------------+--------------------------------+
| **Entries**                                        |
+-------------------+--------------------------------+
| Index             | get_entry                      |
+-------------------+--------------------------------+
| Add               | add_entry                      |
+-------------------+--------------------------------+
| Edit              | edit_entry                     |
+-------------------+--------------------------------+
| Delete            | delete_entry                   |
+-------------------+--------------------------------+
| AddComment        | add_entry_comment              |
+-------------------+--------------------------------+
| EditComment       | edit_entry_comment             |
+-------------------+--------------------------------+
| DeleteComment     | delete_entry_comment           |
+-------------------+--------------------------------+
| Vote              | vote_entry /                   |
|                   | vote_entry_comment             |
+-------------------+--------------------------------+
| Unvote            | unvote_entry /                 |
|                   | unvote_entry_comment           |
+-------------------+--------------------------------+
| **Rank**                                           |
+-------------------+--------------------------------+
| Index             | get_rank                       |
+-------------------+--------------------------------+
| **Observatory**                                    |
+-------------------+--------------------------------+
| Votes             | get_observatory_votes          |
+-------------------+--------------------------------+
| Comments          | get_observatory_comments       |
+-------------------+--------------------------------+
| Entries           | get_observatory_entries        |
+-------------------+--------------------------------+
| EntriesComments   | get_observatory_entres_comments|
+-------------------+--------------------------------+
| **Favorites**                                      |
+-------------------+--------------------------------+
| Index             | get_favorites                  |
+-------------------+--------------------------------+
| Lists             | get_favorites_lists            |
+-------------------+--------------------------------+
| **Stream**                                         |
+-------------------+--------------------------------+
| Index             | get_stream                     |
+-------------------+--------------------------------+
| Hot               | get_stream_hot                 |
+-------------------+--------------------------------+
| **Tag**                                            |
+-------------------+--------------------------------+
| Index             | tag                            |
+-------------------+--------------------------------+
| **PM**                                             |
+-------------------+--------------------------------+
| ConversationsList | get_conversations_list         |
+-------------------+--------------------------------+
| Conversation      | get_conversation               |
+-------------------+--------------------------------+
| SendMessage       | send_message                   |
+-------------------+--------------------------------+
| DeleteConversation| delete_conversation            |
+-------------------+--------------------------------+


Proste żądania
^^^^^^^^^^^^^^^^^^^

Można również skorzystać z podstawowej metody do tworzenia żądań. Przykład z dokumentacji Wykop API będzie przedstawiał się następująco:

::

    link = api.request("link", 'index', [54321,], {"appkey": 12345})

gdzie:

+-------------------+-------------------------+
| 'link'            | typ zasobu              |
+-------------------+-------------------------+
| 'index'           | metoda zasobu           |
+-------------------+-------------------------+
| [54321,]          | lista parametrów metody |
+-------------------+-------------------------+
| {"appkey": 12345} | parametry API           |
+-------------------+-------------------------+

Wykop Connect
^^^^^^^^^^^^^^^^^^^

Możliwe jest też łączenie konta użytkownika z aplikacją

Generowanie linku do Wykop Connect

::

    url = api.get_connect_url("http://hostname.pl")

Dekodowanie danych Wykop Connect

::

    appkey, login, token = api.get_connect_data(encoded_data)

Odpowiedzi
^^^^^^^^^^^^^^^^^^^

Wyróżniamy 3 typy odpowiedzi:

- logiczny, np. metoda observe_profile:
  ::

      >>> print api.observe_profile("m__b")
      [True]

- obiekt, np. metoda get_profile:
  ::

      >>> print api.get_profile("m__b")
      {'author_group': 5, 'buries': None, 'rank': 274, 'links_published': 41, 'gg': '', 'groups': 2, 'entries': 203, .. }

- lista obiektów, np. metoda get_link_digs
  ::

      >> print api.get_link_digs(12345)
      [{'author_group': 2, 'author_sex': 'male', .. }, {'author_group': 2, 'author_sex': 'male', .. }]

Każdy obiekt z odpowiedzi jest typu słownikowego (dict) z możliwością dostępu do właściwości poprzez artybuty:

::

    >> profile = api.get_profile("m__b")
    >> profile["diggs"]
    12155
    >> profile.diggs
    12155

Filtrowanie odpowiedzi
^^^^^^^^^^^^^^^^^^^^^^
Aby odfiltrować z odpowiedzi kod HTML, należy wywołać klasę z parametrem output='clear'

::

    import wykop

    api = wykop.WykopAPI(klucz_aplikacji, sekret_aplikacji, output='clear')
    api.authenticate(login, klucz_polaczenia)
    profile = api.observe_profile("m__b")

API wersja 2
-------------------

Wykop posiada API w wersji 2. Jest to nowa, nieudokumentowana wersja API. Implementacja tej wersji w SDK może się zmieniać.

.. warning::

   Uwierzytelnienie działa tylko z kluczami ze wsparciem dla tej wersji API.

Przykładowe użycie:

::

    from wykop import WykopAPIv2

    api = WykopAPIv2(klucz_aplikacji, sekret_aplikacji)
    profile = api.get_profile("m__b")

Zdefiniowane metody
^^^^^^^^^^^^^^^^^^^

API w wersji 2 posiada następujące wbudowane metody.

+-------------------+--------------------------------+
| Metoda API        | Metoda SDK                     |
+-------------------+--------------------------------+
| **Links**                                          |
+-------------------+--------------------------------+
| ?                 | get_links_promoted             |
+-------------------+--------------------------------+
| ?                 | get_links_upcoming             |
+-------------------+--------------------------------+
| ?                 | get_link_comments              |
+-------------------+--------------------------------+
| ?                 | get_link_related               |
+-------------------+--------------------------------+
| ?                 | get_link_upvoters              |
+-------------------+--------------------------------+
| ?                 | get_link_downvoters            |
+-------------------+--------------------------------+
| **MyWykop**                                        |
+-------------------+--------------------------------+
| ?                 | get_mywykop                    |
+-------------------+--------------------------------+
| ?                 | get_mywykop_tags               |
+-------------------+--------------------------------+
| ?                 | get_mywykop_users              |
+-------------------+--------------------------------+
| **Notifications**                                  |
+-------------------+--------------------------------+
| ?                 | get_notifications              |
+-------------------+--------------------------------+
| ?                 | get_notifications_count        |
+-------------------+--------------------------------+
| ?                 | get_hashtags_notifications     |
+-------------------+--------------------------------+
| ?                 | get_hashtags_notifications_cou |
+-------------------+--------------------------------+
| **Profiles**                                       |
+-------------------+--------------------------------+
| ?                 | get_profile                    |
+-------------------+--------------------------------+
| ?                 | observe_profile                |
+-------------------+--------------------------------+
| ?                 | unobserve_profile              |
+-------------------+--------------------------------+
| ?                 | block_profile                  |
+-------------------+--------------------------------+
| ?                 | unblock_profile                |
+-------------------+--------------------------------+
| **Search**                                         |
+-------------------+--------------------------------+
| ?                 | search_links                   |
+-------------------+--------------------------------+
| ?                 | search_entries                 |
+-------------------+--------------------------------+
| ?                 | search_profiles                |
+-------------------+--------------------------------+
| **Login**                                          |
+-------------------+--------------------------------+
| ?                 | user_login                     |
+-------------------+--------------------------------+
| **Hits**                                           |
+-------------------+--------------------------------+
| ?                 | get_hits_month                 |
+-------------------+--------------------------------+
| ?                 | get_hits_popular               |
+-------------------+--------------------------------+
| **Entries**                                        |
+-------------------+--------------------------------+
| ?                 | get_entry                      |
+-------------------+--------------------------------+
| ?                 | get_stream_entries             |
+-------------------+--------------------------------+
| ?                 | get_hot_entries                |
+-------------------+--------------------------------+
| **Tag**                                            |
+-------------------+--------------------------------+
| ?                 | get_tag                        |
+-------------------+--------------------------------+
| ?                 | get_tags_observed              |
+-------------------+--------------------------------+
| ?                 | get_tag_entries                |
+-------------------+--------------------------------+
| ?                 | get_tag_links                  |
+-------------------+--------------------------------+
| **PM**                                             |
+-------------------+--------------------------------+
| ?                 | get_conversations_list         |
+-------------------+--------------------------------+

? = nieudokumentowana metoda

Proste żądania
^^^^^^^^^^^^^^^^^^^

Implementacja API w wersji 2 również posiada podstawową metodę do tworzenia żądań. Na przykład:

::

    link = api.request("entries", 'hot', {"period": 12})

gdzie:

+-------------------+-------------------------+
| 'entries'         | typ zasobu              |
+-------------------+-------------------------+
| 'hot'             | metoda zasobu           |
+-------------------+-------------------------+
| {"period": 12}    | parametry API           |
+-------------------+-------------------------+

Zgłaszanie błędów
-----------------

Jeżeli znalazłeś jakieś błędy lub masz inny problem zgłoś go na `bugtracker`_ lub na mirko @tenji :>

.. _bugtracker: https://github.com/p1c2u/wykop-sdk/issues
