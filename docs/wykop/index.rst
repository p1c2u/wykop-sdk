Wykop Python SDK
================

Biblioteka ta jest implementacją `Wykop API`_ w Python.

.. _Wykop API: http://www.wykop.pl/developers/api/

Wykop Python SDK jest rozwijane `na GitHub <https://github.com/p1c2u/wykop-sdk/>`_. Twój wkład jest mile widziany!

Wykop Python SDK z założenia ma być prosty
-------------------------------------------

.. code:: python

    import wykop

    api = wykop.WykopAPI(klucz_aplikacji, sekret_aplikacji)
    profile = api.get_profile("m__b")
