musette
=======

``musette`` enables application configuration by providing a proxy to
``os.environ`` which allows:

+ type-casting of environment values
+ updating the environment via plaintext key-value properties files
+ shell-style interpolation

``musette`` is a direct fork of `django-environ`_ with significant changes.
Although it is intended for Django settings configuration it does not actually
require Django itself.

The original module (`django-environ`_) was a merge of:

+ `envparse`_
+ `honcho`_
+ `dj-database-url`_
+ `dj-search-url`_
+ `dj-config-url`_
+ `django-cache-url`_

Basic usage
-----------

::

    from musette import environ

    environ.read('env.properties')

    DEBUG = environ.bool("DEBUG")


Django Settings
---------------

This is your `settings.py` file before you have installed **musette**::

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'database',
            'USER': 'user',
            'PASSWORD': 'githubbedpassword',
            'HOST': '127.0.0.1',
            'PORT': '8458',
        }
        'extra': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'database.sqlite'
        }
    }

    SECRET_KEY = 'notsecret'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                '127.0.0.1:11211', '127.0.0.1:11212', '127.0.0.1:11213',
            ]
        },
        'redis': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': '127.0.0.1:6379:1',
            'OPTIONS': {
                'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
                'PASSWORD': 'redis-githubbed-password',
            }
        }
    }

After::

    from musette import Environment

    env = Environment(DEBUG=(bool, False),)
    env.read('env.properties')

    DEBUG = env('DEBUG') # False if not in os.environ
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': env.db(),
        'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
    }

    SECRET_KEY = env('SECRET_KEY')

    CACHES = {
        'default': env.cache(),
        'redis': env.cache('REDIS_URL')
    }

Properties Files
----------------

A properties or "env" file is plain text file containing one or more
**key := value** or **key = value** lines, where values may optionally
refer to other environment values via shell-style variables::

    that := something
    this := ${that}


How to install
--------------

::

    $ pip install musette


How to use
----------

There is an ``Environment`` class and a convenient instance of that class
called ``environ``.

::

    >>> from musette import Environment
    >>> env = Environment(
            DEBUG=(bool, False),
        )
    >>> env('DEBUG')
    False
    >>> env('DEBUG', default=True)
    True

    >>> open('.myenv', 'a').write('DEBUG=on\n')
    >>> env.read('.myenv')
    >>> env('DEBUG')
    True

    >>> open('.myenv', 'a').write('INT_VAR=1010\n')
    >>> env.read('.myenv')
    >>> env.int('INT_VAR'), env.str('INT_VAR')
    1010, '1010'

    >>> open('.myenv', 'a').write('DATABASE_URL=sqlite:///my-local-sqlite.db\n')
    >>> env.read('.myenv')
    >>> env.db()
    {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'my-local-sqlite.db', 'HOST': '', 'USER': '', 'PASSWORD': '', 'PORT': ''}

``Environment`` by default provides an effective proxy to the ``os.environ``
data dictionary, but you can pass in any other dict instead::

    >>> from musette import Environment
    >>> _environ = {}
    >>> env = Environment(_environ, DEBUG=True)
    >>> _environ['DEBUG']
    True

If you are neither passing in a configuration dict or any schema values then
you can just use the ``environ`` instance::

    >>> import os
    >>> from musette import environ
    >>> set(os.environ.keys()) == set(environ.keys())
    True

Supported Types
---------------

+ str
+ bool
+ int
+ float
+ json
+ list (FOO=a,b,c)
+ dict (BAR=key=val;foo=bar)
+ url
+ db_url
    -  PostgreSQL: postgres://, pgsql://, psql:// or postgresql://
    -  PostGIS: postgis://
    -  MySQL: mysql:// or mysql2://
    -  MySQL for GeoDjango: mysqlgis://
    -  SQLITE: sqlite://
    -  SQLITE with SPATIALITE for GeoDjango: spatialite://
    -  LDAP: ldap://
+ cache_url
    -  Database: dbcache://
    -  Dummy: dummycache://
    -  File: filecache://
    -  Memory: locmemcache://
    -  Memcached: memcache://
    -  Python memory: pymemcache://
    -  Redis: rediscache://
+ search_url
    -  ElasticSearch: elasticsearch://
    -  Solr: solr://
    -  Whoosh: whoosh://
    -  Simple cache: simple://
+ email_url
    -  SMTP: smtp://
    -  SMTPS: smtps://
    -  Console mail: consolemail://
    -  File mail: filemail://
    -  LocMem mail: memorymail://
    -  Dummy mail: dummymail://

Tests
-----

::

    $ git clone git@github.com:averagehuman/musette.git
    $ cd musette
    $ python setup.py test


Credits
-------

- `joke2k`_
- `12factor`_
- `12factor-django`_
- `Two Scoops of Django`_
- `rconradharris`_ / `envparse`_
- `kennethreitz`_ / `dj-database-url`_
- `migonzalvar`_ / `dj-email-url`_
- `ghickman`_ / `django-cache-url`_
- `dstufft`_ / `dj-search-url`_
- `julianwachholz`_ / `dj-config-url`_
- `nickstenning`_ / `honcho`_
- `envparse`_
- `Distribute`_
- `modern-package-template`_

.. _joke2k: http://about.me/danielef
.. _django-environ: https://pypi.python.org/pypi/django-environ

.. _rconradharris: https://github.com/rconradharris
.. _envparse: https://github.com/rconradharris/envparse

.. _kennethreitz: https://github.com/kennethreitz
.. _dj-database-url: https://github.com/kennethreitz/dj-database-url

.. _migonzalvar: https://github.com/migonzalvar
.. _dj-email-url: https://github.com/migonzalvar/dj-email-url

.. _ghickman: https://github.com/ghickman
.. _django-cache-url: https://github.com/ghickman/django-cache-url

.. _julianwachholz: https://github.com/julianwachholz
.. _dj-config-url: https://github.com/julianwachholz/dj-config-url

.. _dstufft: https://github.com/dstufft
.. _dj-search-url: https://github.com/dstufft/dj-search-url

.. _nickstenning: https://github.com/nickstenning
.. _honcho: https://github.com/nickstenning/honcho

.. _12factor: http://www.12factor.net/
.. _12factor-django: http://www.wellfireinteractive.com/blog/easier-12-factor-django/
.. _Two Scoops of Django: https://django.2scoops.org


.. _Distribute: http://pypi.python.org/pypi/distribute
.. _modern-package-template: http://pypi.python.org/pypi/modern-package-template

