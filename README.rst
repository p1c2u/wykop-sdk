Wykop API Python SDK
====================

.. role:: strike
    :class: strike

Biblioteka ta jest implementacją `Wykop API`_ w Python.

.. _Wykop API: http://www.wykop.pl/developers/api/

Przykładowe użycie:

::

    import wykop

    api = wykop.WykopAPI(klucz_aplikacji)
    profile = api.get_profile("m__b")

Uwierzytelnienie 
-------------------

Aby wykonywać działania jako użytkownik zalogowany przed wykonaniem metody należy się uwierzytenić.

Przykładowe użycie metody wymagającej uwierzytelnienia:

::

    import wykop

    api = wykop.WykopAPI(klucz_aplikacji)
    api.authenticate(login, klucz_polaczenia)
    profile = api.observe_profile("m__b")

Zdefiniowane metody 
-------------------

Biblioteka posiada wbudowane metody odpowiednie do zdefiniowanych w Wykop API

+--------------+------------------------+ 
| Metoda API   | Metoda SDK             | 
+==============+========================+ 
| **Comments**                          | 
+--------------+------------------------+ 
| Add          | add_comment            | 
+--------------+------------------------+ 
| Plus         | plus_comment           | 
+--------------+------------------------+
| Minus        | minus_commant          | 
+--------------+------------------------+ 
| Edit         | edit_comment           | 
+--------------+------------------------+
| Delete       | delete_comment         | 
+--------------+------------------------+
| **Link**                              | 
+--------------+------------------------+ 
| Index        | get_link               | 
+--------------+------------------------+ 
| Dig          | dig_link               | 
+--------------+------------------------+ 
| Cancel       | cancel_link            | 
+--------------+------------------------+ 
| Bury         | bury_link              | 
+--------------+------------------------+ 
| Comments     | get_link_comments      | 
+--------------+------------------------+ 
| Reports      | get_link_reports       | 
+--------------+------------------------+ 
| Digs         | get_link_digs          | 
+--------------+------------------------+ 
| Related      | get_link_related       | 
+--------------+------------------------+ 
| Buryreasons  | get_link_buryreasons   | 
+--------------+------------------------+ 
| Observe      | observe_link           | 
+--------------+------------------------+ 
| Favorite     | favorite_link          | 
+--------------+------------------------+
| **Links**                             | 
+--------------+------------------------+ 
| Promoted     | get_links_promoted     | 
+--------------+------------------------+ 
| Upcoming     | get_links_upcoming     | 
+--------------+------------------------+
| **Popular**                           | 
+--------------+------------------------+ 
| Promoted     | get_popular_promoted   | 
+--------------+------------------------+ 
| Upcoming     | get_popular_upcoming   | 
+--------------+------------------------+ 
| **Profile**                           | 
+--------------+------------------------+ 
| Index        | get_profile            | 
+--------------+------------------------+ 
| Added        | get_profile_links      |
+--------------+------------------------+ 
| Published    | get_profile_published  | 
+--------------+------------------------+ 
| Commented    | get_profile_commented  | 
+--------------+------------------------+ 
| Digged       | get_profile_digged     | 
+--------------+------------------------+ 
| Buried       | get_profile_buried     |
+--------------+------------------------+ 
| Observe      | observe_profile        | 
+--------------+------------------------+ 
| Unobserve    | unobserve_profile      | 
+--------------+------------------------+ 
| Followers    | get_profile_followers  | 
+--------------+------------------------+ 
| Followed     | get_profile_followed   | 
+--------------+------------------------+ 
| Favorites    | get_profile_favorites  | 
+--------------+------------------------+ 
| **Search**                            | 
+--------------+------------------------+ 
| Index        | search                 | 
+--------------+------------------------+ 
| Links        | search_links           | 
+--------------+------------------------+ 
| Entries      | search_entries         | 
+--------------+------------------------+ 
| Profiles     | search_profiles        | 
+--------------+------------------------+ 
| **User**                              | 
+--------------+------------------------+ 
| Login        | user_login             | 
+--------------+------------------------+ 
| Favorites    | user_favorites         | 
+--------------+------------------------+ 
| Observed     | user_observed          | 
+--------------+------------------------+ 
| **Entries**                           | 
+--------------+------------------------+ 
| Add          | add_entry              | 
+--------------+------------------------+ 

Proste żądania
-----------------

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

Zgłaszanie błędów
-----------------

Jeżeli znalazłeś jakieś błędy lub masz inny problem zgłoś go na `bugtracker`_

.. _bugtracker: https://github.com/p1c2u/wykop-sdk/issues
