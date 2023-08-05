|Build Status|

ExDoc
=====

Documentation extractor.

Extracts pieces of documentation from your code to build a document
which can be fed to template processors.

Output can be in JSON, YAML, whatever. Use any command-line templating
engine, like `j2cli <https://github.com/kolypto/j2cli>`__, to render
templates from it.

It does not do any automatic background magic: it just offers helpers
which allows you to extract the necessary pieces.

Collectors
==========

ExDoc is just a set of helper functions that collects information into
dictionaries.

Python
------

Helpers for Python objects

doc(obj)
~~~~~~~~

Get parsed documentation for an object as a dict.

This includes arguments spec, as well as the parsed data from the
docstring.

.. code:: python

    from exdoc import doc

The ``doc()`` function simply fetches documentation for an object, which
can be

-  Module
-  Class
-  Function or method
-  Property

The resulting dictionary includes argument specification, as well as
parsed docstring:

.. code:: python

    def f(a, b=1, *args):
        ''' Simple function

        : param a: First
        : type a: int
        : param b: Second
        : type b: int
        : param args: More numbers
        : returns: nothing interesting
        : rtype: bool
        : raises ValueError: hopeless condition
        '''

    from exdoc import doc

    doc(f)  # ->
    {
      'module': '__main__',
      'name': 'f',
      'qualname': 'f',  # qualified name: e.g. <class>.<method>
      'signature': 'f(a, b=1, *args)',
      'qsignature': 'f(a, b=1, *args)',  # qualified signature
      'doc': 'Simple function',
      'clsdoc': '',  # doc from the class (used for constructors)
      # Exceptions
      'exc': [
        {'doc': 'hopeless condition', 'name': 'ValueError'}
      ],
      # Return value
      'ret': {'doc': 'nothing interesting', 'type': 'bool'},
      # Arguments
      'args': [
        {'doc': 'First', 'name': 'a', 'type': 'int'},
        {'default': 1, 'doc': 'Second', 'name': 'b', 'type': 'int'},
        {'doc': 'More numbers', 'name': '*args', 'type': None}
      ],
    }

getmembers(obj, \*predicates)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Return all the members of an object as a list of ``(key, value)``
tuples, sorted by name.

The optional list of predicates can be used to filter the members.

The default predicate drops members whose name starts with '\_'. To
disable it, pass ``None`` as the first predicate.

subclasses(cls, leaves=False)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List all subclasses of the given class, including itself.

If ``leaves=True``, only returns classes which have no subclasses
themselves.

SqlAlchemy
----------

Documenting SqlAlchemy models.

.. code:: python

    from exdoc.sa import doc

    doc(User)  # ->
    {
      'name': 'User',
      # List of tables the model uses
      'table': ('users',),
      'doc': 'User account',
      # PK: tuple[str]
      'primary': ('uid',),
      # Unique keys
      'unique': (
        # tuple[str]
        ('login',),
      ),
      # Foreign keys
      'foreign': (
        {'key': 'uid', 'target': 'users.uid', 'onupdate': None, 'ondelete': 'CASCADE'},
      ),
      # Columns
      'columns': [
        {'key': 'uid', 'type': 'INTEGER NOT NULL', 'doc': ''},
        {'key': 'login', 'type': 'VARCHAR NULL', 'doc': 'Login'},
        {'key': 'creator_uid', 'type': 'INTEGER NULL', 'doc': 'Creator'},
        {'key': 'meta', 'type': 'JSON NULL', 'doc': ''},
      ],
      # Relationships
      'relations': [
        {'key': 'creator', 'model': 'User',
         'target': 'User(creator_uid=uid)', 'doc': ''},
        {'key': 'devices[]', 'model': 'Device',
         'target': 'Device(uid)', 'doc': ''},
        {'key': 'created[]', 'model': 'User',
         'target': 'User(uid=creator_uid)', 'doc': ''},
      ]
    }

Building
========

Create a python file that collects the necessary information and prints
json:

.. code:: python

    #! /usr/bin/env python
    from exdoc import doc
    import json

    from project import User

    print json.dumps({
      'user': doc(User),
    })

And then use its output:

.. code:: console

    ./collect.py | j2 --format=json README.md.j2

.. |Build Status| image:: https://api.travis-ci.org/kolypto/py-exdoc.png?branch=master
   :target: https://travis-ci.org/kolypto/py-exdoc
