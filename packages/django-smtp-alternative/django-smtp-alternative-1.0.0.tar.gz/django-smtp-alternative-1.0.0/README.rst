django-smtp-alternative
=======================

Django email backend providing sending with alternative SMTP server if primary server fails

Installation
------------

.. code:: bash

    pip install django-smtp-alternative


Usage
-----

Edit settings.py

.. code:: python

  EMAIL_BACKEND = "django_smtp_alternative.EmailBackend"

  ALTERNATIVE_EMAIL_HOST = 'alternative.host'
  ALTERNATIVE_EMAIL_PORT = '25'

Following settings are not required, if some is not defined or set to None, is used default settings acording to primary SMTP configuration.

.. code:: python

  ALTERNATIVE_EMAIL_HOST_USER = 'username'
  ALTERNATIVE_EMAIL_HOST_PASSWORD = 'password'
  ALTERNATIVE_EMAIL_USE_TLS = False

License
-------

LGPLv3
