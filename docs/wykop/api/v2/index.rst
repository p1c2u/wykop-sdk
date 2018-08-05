API wersja 2
------------

Wykop posiada API w wersji 2.

.. warning::

   Jest to nieudokumentowana wersja API. Implementacja tej wersji w SDK może się zmieniać.

.. warning::

   Uwierzytelnienie działa tylko z kluczami ze wsparciem dla tej wersji API.

Przykładowe użycie:

::

    from wykop import WykopAPIv2

    api = WykopAPIv2(klucz_aplikacji, sekret_aplikacji)
    profile = api.get_profile("m__b")


.. toctree::

   methods
   requests
