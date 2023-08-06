db.py
=====

.. code:: python

    >>> from db import DB
    >>> db = DB(username="greg", password="secret", hostname="localhost",
                dbtype="postgres")
    >>> db.save_credentials(profile="local")

