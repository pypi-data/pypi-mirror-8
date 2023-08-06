ObjectPath
==========

`|Downloads| <https://pypi.python.org/pypi/objectpath/>`_
`|License| <https://pypi.python.org/pypi/objectpath/>`_ `|Build
Status| <https://travis-ci.org/adriank/ObjectPath>`_ `|Code
Health| <https://landscape.io/github/adriank/ObjectPath/master>`_
`|Coverage
Status| <https://coveralls.io/r/adriank/ObjectPath?branch=master>`_

The agile NoSQL query language for semi-structured data
-------------------------------------------------------

**#Python #NoSQL #Javascript #JSON #nested-array-object**

ObjectPath is a query language similar to XPath or JSONPath, but much
more powerful thanks to embedded arithmetic calculations, comparison
mechanisms and built-in functions. This makes the language more like SQL
in terms of expressiveness, but it works over JSON documents rather than
relations. ObjectPath can be considered a full-featured expression
language. Besides selector mechanism there is also boolean logic, type
system and string concatenation available. On top of that, the language
implementations (Python at the moment; Javascript is in beta!) are
secure and relatively fast.

More at `ObjectPath site <http://objectpath.org/>`_

.. figure:: http://adriank.github.io/ObjectPath/img/op-colors.png
   :align: center
   :alt: ObjectPath img

   ObjectPath img
ObjectPath makes it easy to find data in big nested JSON documents. It
borrows the best parts from E4X, JSONPath, XPath and SQL. ObjectPath is
to JSON documents what XPath is to XML. Other examples to ilustrate this
kind of relationship are:

==============  ==================
Scope           Language
==============  ==================
text documents  regular expression
XML             XPath
HTML            CSS selectors
JSON documents  ObjectPath
==============  ==================

Documentation
-------------

`ObjectPath Reference <http://objectpath.org/reference.html>`_

What's in this repo?
--------------------

ObjectPathPY - Python implementation of ObjectPath, used in production
for over two years without problems. Use objectpath.py file as a example
of usage.

ObjectPathJS - beta version of Javascript implementation. Many tests
passed, {} and functions are not implemented yet. Javascript
implementation has the very same API as the Python version.

Command line usage
------------------

``sh $ sudo pip install objectpath $ objectpath file.json`` or
``sh $ git clone https://github.com/adriank/ObjectPath.git $ cd ObjectPath $ python shell.py file.json``

Python usage
------------

::

    $ sudo pip install objectpath
    $ python
    >>> from objectpath import *
    >>> tree=Tree({"a":1})
    >>> tree.execute("$.a")
    1
    >>>

::

    $ git clone https://github.com/adriank/ObjectPath.git
    $ cd ObjectPath
    $ python
    >>> from objectpath import *
    >>> tree=Tree({"a":1})
    >>> tree.execute("$.a")
    1
    >>>

License
-------

**AGPLv3**

Using ObjectPath language in your project does not mean that your
project is a derivative work, provided that you don't - extend the
language functionality, - make optimizations, - sub-class any of it's
modules.

AGPL v3 license has been chosen to ensure language consistency and
provide a way to finance its development.

**If AGPL v3 is too restrictive for you, please consider buying a
commercial licenses provided by Asyncode. This is the preferred way of
supporting this project financially.**

.. |Downloads| image:: https://pypip.in/download/objectpath/badge.svg
.. |License| image:: https://pypip.in/license/objectpath/badge.svg
.. |Build
Status| image:: https://travis-ci.org/adriank/ObjectPath.svg?branch=master
.. |Code
Health| image:: https://landscape.io/github/adriank/ObjectPath/master/landscape.png
.. |Coverage
Status| image:: https://coveralls.io/repos/adriank/ObjectPath/badge.png?branch=master

Download
********


