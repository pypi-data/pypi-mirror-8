====================
Django Arakoon Cache
====================

`Arakoon <http://arakoon.org/>`_ cache backend for Django.

Install
-------

::

    pip install https://github.com/Incubaid/arakoon/archive/1.6.0.tar.gz
    pip install django-arakoon-cache


Development
-----------

To run tests, there is a test django app **cache_app** used for testing ArakoonCache.

Make sure you run an Arakoon cluster with 3 nodes, running on the sample config found in **arakoon/conf/arakoon.ini**.

::

    pip install -r requirements.txt
    python tests/manage.py test cache_app


Django settings
---------------

This is an example of configuring django to use **ArakoonCache** as a cache backend.

Assuming we are running an Arakoon cluster of 3 nodes.

::

    CACHES = {
        'default': {
            'BACKEND': 'django_arakoon_cache.cache.ArakoonCache',
            'LOCATION': {
                'arakoon_0': ('127.0.0.1', 4000),
                'arakoon_1': ('127.0.0.1', 4001),
                'arakoon_2': ('127.0.0.1', 4002)
            },
            'OPTIONS': {
                'cluster': 'django'
            }
        }
    }
