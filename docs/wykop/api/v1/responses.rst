Odpowiedzi
^^^^^^^^^^

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