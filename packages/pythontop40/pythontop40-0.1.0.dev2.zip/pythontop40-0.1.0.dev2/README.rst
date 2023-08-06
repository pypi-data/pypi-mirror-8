PythonTop40
===========

The **PythonTop40** library is designed to be used in UK schools to provide programmatic access to data that
describes the UK Top 40 singles and albums. The hope is that by providing simple interfaces to access
information that students may have an interest in, they may be inspired to code-further.

**PythonTop40** is written in python and currently **ONLY SUPPORTS PYTHON 3**.

**PythonTop40** is under active development (visit `this blog post <http://www.onebloke.com/2014/12/pythontop40-get-the-uk-top-40-albums-and-singles-from-python/>`_ for more information.) and licensed under the `Apache2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_, so feel free to `contribute <https://bitbucket.org/dannygoodall/pythontop40/pull-requests>`_ and `report errors and suggestions <https://bitbucket.org/dannygoodall/pythontop40/issues>`_.

Usage
-----
**PythonTop40** exposes a very simple API to developers. It is accessed by importing the :class:`Top40` into your module
and creating an instance of this class, like so::

   from pythontop40 import Top40
   top40 = Top40()

The ``top40`` instance exposes a number of properties to the programmer. These include:

* ``top40.albums``
* ``top40.singles``
* ``top40.singles_chart``
* ``top40.albums_chart``

The example code below shows how you can use one of these properties to get a list of the current Top 40 albums.::

   from pythontop40 import Top40

   top40 = Top40()

   albums = top40.albums

   for album in albums:
       print(
           album.position,
           album.title,
           "BY",
           album.artist
       )

This short program imports from the Top40 api using the ``Top40.albums`` property, and then loops
through each album entry and prints a short summary to the console.

Tests
-----

To run the Booby test suite you should install the development requirements and then run nosetests.

.. code-block:: bash

    $ pip install -r test-requirements.txt
    $ nosetests tests

Changes
-------

See `Changes <https://booby.readthedocs.org/en/latest/changes.html>`_.
=======
PythonTop40
===========

The **PythonTop40** library is designed to be used in UK schools to provide students with access to data that describes
the UK Top 40 singles and albums.

This is part of a wider initiative that I'm referring to as **Code-Further**. The hope is that by providing simple
interfaces to information that is relevant to students, they will be able to relate to the data and imagine more
ways in which they could consume and use it in their code - and hopefully **Code-Further**.

The data that **PythonTop40** accesses is provided by the excellent work by
`@Ben Major <https://twitter.com/benmajor88>`_ and his
`UK Top 40 Charts API <http://ben-major.co.uk/2013/12/uk-top-40-charts-api/>`_.

**PythonTop40** is under active development visit
`this blog post <http://www.onebloke.com/2014/12/pythontop40-get-the-uk-top-40-albums-and-singles-from-python/>`_
for more information. and licensed under the `Apache2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_,
so feel free to `contribute <https://bitbucket.org/dannygoodall/pythontop40/pull-requests>`_ and
`report errors and suggestions <https://bitbucket.org/dannygoodall/pythontop40/issues>`_.

.. note::
    The **PythonTop40** library is designed to be used in UK schools to provide programmatic access to data that
    describes the UK Top 40 singles and albums. The hope is that by providing simple interfaces to access
    information that students may have an interest in, they may be inspired to **code-further**.
    This documentation will therefore most likely be aimed at teachers and education professionals, who may not have a
    deep knowledge of Python.

.. warning::
    **PythonTop40** is currently designed to work with Python version 3. An effort to make it work with both
    Python 2 and 3 is planned, but as I have no experience of code that works in both environments, this will be a lower
    priority. I'd welcome `contributions from other developers
    <https://bitbucket.org/dannygoodall/pythontop40/pull-requests>`_ on this.

Usage
-----
**PythonTop40** exposes a very simple API to developers. It is accessed by importing the :class:`~top40.Top40`
class into your module and creating an instance of this class, like so::

   from pythontop40 import Top40
   top40 = Top40()

The ``top40`` instance exposes a number of properties to the programmer. These include:

* :py:attr:`top40.albums <top40.Top40.albums>`
* :py:attr:`top40.singles <top40.Top40.singles>`
* :py:attr:`top40.albums_chart <top40.Top40.albums_chart>`
* :py:attr:`top40.singles_chart <top40.Top40.singles_chart>`

The example code below shows how you can use one of these properties to get a list of the current Top 40 albums.::

   from pythontop40 import Top40

   top40 = Top40()

   albums = top40.albums

   for album in albums:
       print(
           album.position,
           album.title,
           "BY",
           album.artist
       )

This short program uses the :py:attr:`~top40.Top40.albums` property of the :class:`~top40.Top40`
class to obtain the Python :class:`list` of the current Top 40 UK albums. It then loops through this list, and at each
iteration of the loop the variable `album` is set to the next album entry in the list.

A :func:`print` function then prints the :py:attr:`~top40.Entry.position`,
:py:attr:`~top40.Entry.title` and :py:attr:`~top40.Entry.artist` attributes of the album
:py:class:`entry <top40.Entry>` resulting in something like this:::

    1 Never Been Better BY Olly Murs
    2 X BY Ed Sheeran
    3 FOUR BY One Direction
    4 In The Lonely Hour BY Sam Smith
    5 The Endless River BY Pink Floyd
    .
    .
    .
    40 The London Sessions BY Mary J. Blige


I hope it's pretty clear what is going on, but a more detailed discussion of what the program does on can be found
:doc:`here <moredetail>`.

Features
========
**PythonTop40** provides:

* a list of the current Top 40 UK singles using the :py:attr:`singles <top40.Top40.singles>` property of the
  :py:class:`~top40.Top40` class.
* a list of the current Top 40 UK albums using the :py:attr:`albums <top40.Top40.singles>` property of the
  :py:class:`~top40.Top40` class.
* a :py:class:`chart <top40.Chart>` object relating to either singles or albums. The
  :py:class:`chart <top40.Chart>` object contains the:

  *  :py:attr:`~top40.Chart.date` that the chart was published
  *  the date that the chart was :py:attr:`~top40.Chart.retrieved` from the server
  *  a :py:class:`list` containing an :py:class:`~top40.Entry` for each Top 40 single or album

* **PythonTop40** will also cache the results, so that once a result type (singles or albums) has been retrieved from
  the remote server, it will be returned on subsequent requests from the cache without refreshing from the remote
  server.
* The cache can be reset using the :py:func:`~top40.Top40.reset_cache` method, so that the next request for
  albums or singles information will be forced to obtain it by connecting to the remote server.

Installation
============
Currently, installing **PythonTop40** involves using the
`development version on BitBucket <https://bitbucket.org/dannygoodall/pythontop40/>`_. The project will eventually be
uploaded to PyPI so that it can be downloaded using ``pip``.

API - Application Programming Interface
=======================================
The full documentation of the classes and functions that make up **PythonTop40** can be found :doc:`here <top40>`, the
errors and exceptions can be found :doc:`here <errors>` and the utility functions are :doc:`here <utils>`.

Tests
-----
To run the **PythonTop40** test suite, you should install the test and development requirements and then run nosetests.

.. code-block:: bash

    $ pip install -r dev-requirements.txt
    $ nosetests tests

Changes
-------

See :doc:`Changes <changes>`.
>>>>>>> 3f273292e03d1852ced37319d49628812ca206af
