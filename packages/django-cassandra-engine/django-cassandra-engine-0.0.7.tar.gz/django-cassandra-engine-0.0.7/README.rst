
Django Cassandra Engine
=======================

.. image:: https://pypip.in/version/django-cassandra-engine/badge.svg
    :target: https://pypi.python.org/pypi/django-cassandra-engine/
    :alt: Latest Version
.. image:: https://travis-ci.org/r4fek/django-cassandra-engine.svg?branch=master
    :target: https://travis-ci.org/r4fek/django-cassandra-engine
.. image:: https://pypip.in/download/django-cassandra-engine/badge.svg
    :target: https://pypi.python.org/pypi//django-cassandra-engine/
    :alt: Downloads

django-cassandra-engine is a database wrapper for Django Framework.
It uses latest `Cqlengine <https://github.com/cqlengine/cqlengine>`_ which is currently the best Cassandra CQL 3 Object Mapper for Python.

:License: 2-clause BSD
:Keywords: django, cassandra, orm, nosql, database, python
:URL (pypi): `django-cassandra-engine <https://pypi.python.org/pypi/django-cassandra-engine>`_

Requirements
------------

- cassandra
- cqlengine
- django-nonrel
- djangotoolbox
- django (1.6 or 1.7)


Features
--------

- complete Django integration
- working syncdb and flush commands
- support for creating/destroying test database
- accept all Cqlengine connection options
- automatic connection/disconnection handling
- support for multiple databases (also relational)


Installation
------------

Recommended installation::

   pip install django-cassandra-engine
  

Usage
-----

#. Add django-cassandra-engine to ``INSTALLED_APPS`` in your settings.py file::

    INSTALLED_APPS += ('django_cassandra_engine',)
   

IMPORTANT: This app should be last on ``INSTALLED_APPS`` list.

#. Also change ``DATABASES`` setting::

    DATABASES = {
        'default': {
            'ENGINE': 'django_cassandra_engine',
            'NAME': 'db',
            'TEST_NAME': 'test_db',
            'HOST': 'db1.example.com,db2.example.com',
            'OPTIONS': {
                'replication': {
                    'strategy_class': 'SimpleStrategy',
                    'replication_factor': 1
                }
            }
        }
    }


#. Define some model::

    #  myapp/models.py
    import uuid
    from cqlengine import columns
    from cqlengine.models import Model

    class ExampleModel(Model):
        read_repair_chance = 0.05 # optional - defaults to 0.1
        example_id      = columns.UUID(primary_key=True, default=uuid.uuid4)
        example_type    = columns.Integer(index=True)
        created_at      = columns.DateTime()
        description     = columns.Text(required=False)

#. Run ``./manage.py syncdb``
#. Done!


Advanced usage
--------------

Sometimes you want to use cassandra database along with your RDMS.
This is also possible! Just define your DATABASES like here::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'cassandra': {
            'ENGINE': 'django_cassandra_engine',
            'NAME': 'db',
            'TEST_NAME': 'test_db',
            'HOST': '127.0.0.1',
            'OPTIONS': {
                'replication': {
                    'strategy_class': 'SimpleStrategy',
                    'replication_factor': 1
                },
                'connection': {
                    'consistency': ConsistencyLevel.ONE,
                    'lazy_connect': False,
                    'retry_connect': False
                    # + All connection options for cassandra.Cluster()
                }
            }
        }
    }

Then run ``./manage.py syncdb`` for your regular database and
``./manage.py syncdb --database cassandra`` for Cassandra DB.

Links
-----

* `Changelog`_


.. _Changelog: https://github.com/r4fek/django-cassandra-engine/blob/master/CHANGELOG.rst
