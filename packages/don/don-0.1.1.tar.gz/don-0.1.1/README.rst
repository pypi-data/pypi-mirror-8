DON - Dot Object Notation
=========================

DON stands for Dot Object Notation. It is a convenient way to write
simple configuration files.

.. image:: https://travis-ci.org/susam/don.svg?branch=master
   :target: https://travis-ci.org/susam/don

.. image:: https://img.shields.io/coveralls/susam/don.svg
   :target: https://coveralls.io/r/susam/don

.. contents::
   :backlinks: none

Requirements
------------
This module should be used with Python 3.4 or any later version of
Python interpreter.

This module depends only on the Python standard library. It does not
depend on any third party libraries.

Installation
------------
You can install this package using pip3 using the following command. ::

    pip3 install don

You can install this package from source distribution. To do so,
download the latest .tar.gz file from https://pypi.python.org/pypi/don,
extract it, then open command prompt or shell, and change your current
directory to the directory where you extracted the source distribution,
and then execute the following command. ::

    python3 setup.py install

Note that on a Windows system, you may have to replace ``python3`` with
the path to your Python 3 interpreter.

Support
-------
To report any bugs, or ask any question, please visit
https://github.com/susam/don/issues.

Resources
---------
Here is a list of useful links about this project.

- `Latest release on PyPI <https://pypi.python.org/pypi/don>`_
- `Source code on GitHub <https://github.com/susam/don>`_
- `Issue tracker on GitHub <https://github.com/susam/don/issues>`_
- `Changelog on GitHub
  <https://github.com/susam/don/blob/master/CHANGES.rst>`_

License
-------
This is free software. You are permitted to redistribute and use it in
source and binary forms, with or without modification, under the terms
of the Simplified BSD License. See the LICENSE.rst file for the complete
license.

This software is provided WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
LICENSE.rst file for the complete disclaimer.


Tutorial
========

Getting started
---------------
Here is a very simple example of DON. ::

    title: Countries

    india.capital: New Delhi
    india.demonym: Indian
    india.driving: Left

    italy.capital: Rome
    italy.demonym: Italian
    italy.driving: Right

The above DON specifies three top-level DON attributes (also known as
root attributes). They are ``title``, ``india`` and ``italy``. The
``title`` attribute is a string attribute. The value of ``title`` is
``Countries``. However, ``india`` and ``italy`` are object attributes.
The value of ``india`` is an object which contains three attributes:
``capital``, ``demonym`` and ``driving``.

The root object is an object of type ``don.Object``. This is a
dictionary that supports accessing its keys as attributes as well.
Therefore, for the above example, ``title``, ``india`` and ``italy`` are
keys in the root object. The value of string attributes are of type
``str``. The value of object attributes are of type ``don.Object``.

The following Python code demonstrates how the ``don`` module may be
used to parse the above example DON into a root DON object, and then
access the attributes.

.. code:: python

    import don

    # An example DON
    s = """
    title: Countries

    india.capital: New Delhi
    india.demonym: Indian
    india.driving: Left

    italy.capital: Rome
    italy.demonym: Italian
    italy.driving: Right
    """

    # Parse DON
    root = don.parse(s)

    # Access a root attribute
    print(root.title)

    # Access object attributes in various ways
    print(root.india.capital)       # As attributes
    print(root['india']['demonym']) # As dictionary keys
    print(root.india['driving'])    # In a mixed fashion

    # An object attribute is actually a dictionary
    print(root.italy)

Here is the output of the above program. ::

    Countries
    New Delhi
    Indian
    Left
    {'driving': 'Right', 'capital': 'Rome', 'demonym': 'Italian'}

This is all there is to parsing a DON string into an object and
accessing its attributes.

DON syntax
----------
A DON string or DON file contains a list of key value pairs. Each key
value pair is separated by a colon. Here is an example. ::

    fruit: mango
    drink: beer
    level: debug

Empty lines, lines consisting of whitespace characters only and lines
beginning with the hash character, i.e. ``#``, are ignored. Therefore,
lines beginning with ``#`` may be used to write comments. The following
DON example is equivalent to the previous example. ::

    # Eat and drink
    fruit: mango
    drink: beer

    # Logging level
    level: debug

Further, any leading whitespace before a key or a value, and any
trailing whitespace after a key or value are ignored. The following DON
example is equivalent to the previous example. ::

    # Eat and drink
      fruit : mango
        drink: beer

      # Logging level
    level:debug

A DON string represents a single object, known as the root object, that
contains attributes. For example, when the above example is parsed by
DON parser, the string is converted into a root object (which we will
call as ``root``). This root object in turn contains three attributes
with three values. In this case, all three values happen to be strings,
so these attributes may be called string attributes.

The keys in DON may be one or more dot separated tokens. Each token must
be a valid Python identifier. Here is an example that shows dot
separated tokens as keys. ::

    process.priority: normal
    process.protocol: tcp
    process.log.file: log.txt
    process.log.level: debug
    process.log.rotate: daily

In this example, the root object contains an object attribute called
``process`` which in turn contains two string attributes called
``priority`` and ``protocol``, and one object attribute called ``log``.
The ``log`` attribute in turn contains three string attributes called
``file``, ``level`` and ``rotate``.

Here is a tree diagram that shows the relationship between the various
attributes. ::

    (root)
     `-- process
         |-- priority
         |-- protocol
         `-- log
             |-- file
             |-- level
             `-- rotate

This is a DON tree. The root node is known as the root object. The
internal nodes are always object attributes. They contain one or more
other attributes as their values. The leaf nodes are always string
attributes. They contain strings as their values.

A key may contain one or more empty tokens before any non-empty token.
An empty token in a key is equivalent to the corresponding token in its
previous key, i.e. the Nth empty token in a key is a synonym for the Nth
token in its previous key. An empty token must appear before any
non-empty token. The number of empty tokens in a key must not exceed the
number of tokens in its previous key. According to these rules, the
following DON example is equivalent to the previous example. ::

    process.priority: normal
    .protocol: tcp
    .log.file: log.txt
    ..level: debug
    ..rotate: daily

Since leading and trailing whitespace characters around keys and values
are ignored, the keys with empty tokens may be indented to improve
readability. ::

    process.priority: normal
           .protocol: tcp 
           .log.file: log.txt
              ..level: debug
              ..rotate: daily

When a key is followed by empty value, it only declares the key. It does
not define anything. It does not cause the DON tree to be updated.
Declaring a key is useful for using empty tokens in the following keys,
so that the empty tokens in the following keys become synonyms of the
corresponding tokens in the declared key. This can improve readability
quite significantly as shown by the following DON example which is
equivalent to the previous example. ::

    process:
        .priority: normal
        .protocol: tcp 
        .log:
            ..file: log.txt
            ..level: debug
            ..rotate: daily
