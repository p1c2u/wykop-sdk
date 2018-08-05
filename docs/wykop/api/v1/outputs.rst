Filtrowanie odpowiedzi
^^^^^^^^^^^^^^^^^^^^^^
Aby odfiltrować z odpowiedzi kod HTML, należy wywołać klasę z parametrem output='clear'

::

    import wykop

    api = wykop.WykopAPI(klucz_aplikacji, sekret_aplikacji, output='clear')
    api.authenticate(login, klucz_polaczenia)
    profile = api.observe_profile("m__b")