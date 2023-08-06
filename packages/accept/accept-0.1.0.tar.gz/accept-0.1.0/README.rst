accept
======


.. image:: https://travis-ci.org/rhyselsmore/accept.png?branch=master
        :target: https://travis-ci.org/rhyselsmore/accept

.. image:: https://pypip.in/d/accept/badge.png
        :target: https://pypi.python.org/pypi/accept


A simple library for parsing and ordering a HTTP Accept header.

Includes parameter extraction.


Installation
------------

.. code-block:: bash

    pip install accept

Or if you *must* use easy_install:

.. code-block:: bash

    alias easy_install="pip install $1"
    easy_install accept


Usage
-----

.. code-block:: python

    >>> import accept
    >>> accept.parse("text/*, text/html, text/html;level=1, */*")
    [<Media Type: text/html; q=1.0; level=1>, <Media Type: text/html; q=1.0>, <Media Type: text/*; q=1.0>, <Media Type: */*; q=1.0>]
    >>> d = accept.parse("application/json; version=1; q=1.0; response=raw")[0]
    >>> d.media_type
    'application/json'
    >>> d.quality
    1.0
    >>> d.q
    1.0
    >>> d.params
    {'version': '1', 'response': 'raw'}
    >>> d['version']
    '1'
    >>> d['potato']
    None


Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. There is a Contributor Friendly tag for issues that should be ideal for people who are not very familiar with the codebase yet.
#. Fork `the repository`_ on Github to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published.

.. _`the repository`: http://github.com/rhyselsmore/accept
