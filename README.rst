Wykop API Python SDK
=========

Biblioteka ta jest implementacją `Wykop API`_ w Python.

.. _Wykop API: http://www.wykop.pl/developers/api/

Przykładowe użycie:

::

	import wykop

    api = wykop.WykopAPI(appkey)
    profile = api.get_profile("m__b")

Zdefiniowane metody 
-----------------

Biblioteka posiada wbudowane metody odpowiednie do zdefiniowanych w Wykop API

+--------------+-------------------+ 
| Metoda API   | Metoda SDK        | 
+==============+===================+ 
| Profile                          | 
+==============+===================+ 
| Index        | get_profile       | 
+--------------+-------------------+ 
| Added        | get_profile_links |
+--------------+-------------------+ 
| User                             | 
+==============+===================+ 
| Login        | user_login        | 
+--------------+-------------------+ 

Proste żądania
-----------------

Można również skorzystać z podstawowej metody do tworzenia żądań. Przykład z dokumentacji Wykop API będzie przedstawiał się następująco:

::

	link = api.request("link", 'index', [54321,], {"appkey": 12345})

gdzie:

'link'              typ zasobu
'index'             metoda zasobu
[54321,]            lista parametrów metody
{"appkey": 12345}   parametry API

Zgłaszanie błędów
-----------------

Jeżeli znalazłeś jakieś błędy lub masz inny problem zgłoś go na `bugtracker`_

.. _Wykop API Python SDK bugtracker: https://github.com/p1c2u/wykop-sdk/issues
