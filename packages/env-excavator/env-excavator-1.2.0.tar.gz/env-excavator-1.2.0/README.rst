=============================
env-excavator
=============================

.. image:: https://badge.fury.io/py/env-excavator.png
    :target: https://badge.fury.io/py/env-excavator

.. image:: https://travis-ci.org/simpleenergy/env-excavator.png?branch=master
    :target: https://travis-ci.org/simpleenergy/env-excavator

Tools for exconverting environment variables to native python objects

Quickstart
----------

Install env-excavator::

    pip install env-excavator

Example use it in a project::

    >>> import os
    >>> import excavator
    >>> os.environ['FROM_EMAIL'] = 'admin@example.com'
    >>> excavator.env_string('FROM_EMAIL')
    ... 'admin@example.com'
    >>> os.environ['DEBUG'] = 'True'
    >>> DEBUG = excavator.env_bool('DEBUG')
    ... True
    >>> os.environ['ALLOWED_HOSTS'] = '.example.com,.example.net'
    >>> excavator.env_list('ALLOWED_HOSTS')
    ['.example.com', '.example.net']

API
---

* ``excavator.env_string(name, required=False, default='')``::

  Pulls an environment variable out of the environment returning it as a string.

  **name** - the name of the environment variable be pulled

  **required** - Whether the environment variable is required.  If ``True`` and
  the variable is not present, a ``KeyError`` is raised.

  **default** - The value to return if the environment variable is not present.
  (providing a default alongside setting ``required=True`` will raise a
  ``ValueError``)

* ``excavator.env_bool(name, truthy_values=('True', 'true'), required=False, default='')``::

  Pulls an environment variable out of the environment returning it as a
  boolean.  The strings ``'True'`` and ``'true'`` are the default *truthy*
  values.

  **name** - the name of the environment variable be pulled
  
  **truthy_values** - An iterable of values that should be considered truthy.

  **required** - Whether the environment variable is required.  If ``True`` and
  the variable is not present, a ``KeyError`` is raised.

  **default** - The value to return if the environment variable is not present.
  (providing a default alongside setting ``required=True`` will raise a
  ``ValueError``)

* ``excavator.env_list(name, separator=',', required=False, default='')``::

  Pulls an environment variable out of the environment, splitting it on a
  separator, and returning it as a list.  Extra whitespace on the list values
  is stripped.  List values that evaluate as falsy are removed.

  **name** - the name of the environment variable be pulled
  
  **separator** - The separator that the string should be split on.

  **required** - Whether the environment variable is required.  If ``True`` and
  the variable is not present, a ``KeyError`` is raised.

  **default** - The value to return if the environment variable is not present.
  (providing a default alongside setting ``required=True`` will raise a
  ``ValueError``)
