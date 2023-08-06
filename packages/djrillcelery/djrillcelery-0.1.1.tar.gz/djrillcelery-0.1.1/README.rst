DjrillCelery
===============================================

DjrillCelery extends the `Djrill <https://github.com/brack3t/Djrill>`_ package with a backend that sends mail with celery tasks.

**Prerequisites**

* Install Djrill: https://djrill.readthedocs.org/en/latest/
* Install Celery: https://pypi.python.org/pypi/djrill

Quickstart
------------

1. Install DjrillCelery from PyPI:

   .. code-block:: console

        $ pip install djrillcelery


2. Edit your project's ``settings.py``:

   .. code-block:: python

        INSTALLED_APPS = (
            ...
            "djrillcelery"
        )

        EMAIL_BACKEND = "djrillcelery.mail.backends.DjrillCeleryBackend"


3. Now, for every mail that is sent a new task is created.


