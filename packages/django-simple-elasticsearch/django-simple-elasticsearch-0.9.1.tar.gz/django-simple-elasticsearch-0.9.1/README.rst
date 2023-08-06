===========================
Django Simple Elasticsearch
===========================

.. image:: https://badge.fury.io/py/django-simple-elasticsearch.png
    :target: http://badge.fury.io/py/django-simple-elasticsearch

.. image:: https://travis-ci.org/jaddison/django-simple-elasticsearch.png?branch=master
        :target: https://travis-ci.org/jaddison/django-simple-elasticsearch

.. image:: https://pypip.in/d/django-simple-elasticsearch/badge.png
        :target: https://pypi.python.org/pypi/django-simple-elasticsearch


NOTE: The 0.5.x version codebase is deprecated and no longer supported. Version 0.9+ is a breaking change release.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


This package provides a simple method of creating Elasticsearch indexes for
Django projects.

* Free software: BSD license

Features
--------

* class mixin containing mainly `@classmethod` methods to handle index, type,
  mapping, and document data generation for indexing/deletion purposes
* optionally auto index/delete with model signals (can trigger manual
  indexing of data - there are great use cases for this)
* management command to handle broad initialization and indexing

TODO
----

* Update all the RST template files appropriately. audreyr's `cookiecutter`
  was used to generate the base files in this package.
* Tests. Write them.
* Documentation. Write it.
