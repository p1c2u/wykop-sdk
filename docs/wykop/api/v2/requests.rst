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