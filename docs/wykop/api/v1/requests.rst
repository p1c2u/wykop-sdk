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