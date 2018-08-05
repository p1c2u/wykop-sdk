Wykop Connect
^^^^^^^^^^^^^

Możliwe jest też łączenie konta użytkownika z aplikacją

Generowanie linku do Wykop Connect

::

    url = api.get_connect_url("http://hostname.pl")

Dekodowanie danych Wykop Connect

::

    appkey, login, token = api.get_connect_data(encoded_data)