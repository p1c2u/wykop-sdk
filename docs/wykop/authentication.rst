Uwierzytelnienie
-------------------

Aby wykonywać działania jako użytkownik zalogowany przed wykonaniem metody należy się uwierzytenić.

Przykładowe użycie metody wymagającej uwierzytelnienia:

::

    import wykop

    api = wykop.WykopAPI(klucz_aplikacji, sekret_aplikacji)
    api.authenticate(login, klucz_polaczenia)
    profile = api.observe_profile("m__b")