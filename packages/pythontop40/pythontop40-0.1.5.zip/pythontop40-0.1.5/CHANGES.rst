Change Log for **PythonTop40**
==============================

v0.1.5 29th December 2014
-------------------------
* Minor change. Bumped version number. Updated changes docs. Testing the automated build from a bitbucket push.

v0.1.4 29th December 2014
-------------------------
* Minor change. Removed the embedded test-requirments requirement from the dev-requirements.txt file.

v0.1.3 29th December 2014
-------------------------
* Minor change. Modified install_requires list. Removed nap and munch. Added requests-cache.

v0.1.2 29th December 2014
-------------------------
* Top40HTTPError now defaults to return_code=0
* Added the request-cache sqlite file to .gitignore
* Added requests-cache to requirements.txt
* Removed munch and nap from requirements.txt
* Added httpretty to test-requirements.txt
* Refactored errors returned when reading from the remote server
* Refactored tests away from mock and to use httpretty instead
* Implemented requests-cache. This should be seamless with existing code and will now persist results to local sqlite
  storage with a cache duration of 3600 seconds (one hour)
* Added option to pass an extended persistent_cache_config dictionary, which will be passed to the request_cache
  instance - this should allow for other cache types to sqlite.
* Removed the code to recursively create a Munch structure, Python native dicts are now used
* Removed the code to create a nap api object to access the remote server, and instead have replaced it with pure
  requests access. This was overkill for this project.
* Changed documentation
* Removed utils module and associated documentation
* Changed CHANGES.RST to CHANGES.rst
* Bumped version to 0.1.2

v0.1.1 14th December 2014
-------------------------
* Fix for TypeError 'encoding' is an invalid keyword argument for this function - trying to install PythonTop40 on Python 2.7

v0.1.0 13th December 2014
-------------------------
* Minor changes to the documentation relating to Python 2 status
* First official release

v0.1.0.dev9 - 12th December 2014
--------------------------------
* Updated docs from previous change
* First cut at a Python 2 version. Need to create more tests so that I have greater coverage, but passing so far
* Changes to demo code so that it will run in V2 or V3
* Removed python3_compat.py
* Created extra dependencies - six and future
* Increased version number to v0.1.0.dev9

v0.1.0.dev8 - 12th December 2014
--------------------------------
* Added optional field "current" to the Chart model - used in V2 of the API, but not in V1
* Increased version number to v0.1.0.dev8

v0.1.0.dev7 - 11th December 2014
--------------------------------
* Refactoring of Doc generation and setup.py - both now get config information from package_info.json
* Increased version number to v0.1.0.dev7

v0.1.0.dev6 - 11th December 2014
--------------------------------
* Added an optional field "status" to the Entry model - This will be filled in using V2 of the API, but will be not present for V1.
* Added Test changes to ensure "status" field can be present or non-present.
* Increased version number to v0.1.0.dev6

v0.1.0.dev5 - 8th December 2014
-------------------------------
* Removed requirement for development version of Booby from setup.py
* Removed the trailing slash from the URL for /singles and /albums

v0.1.0.dev4 - 6th December 2014
-------------------------------
* Changed the way the setuptools ``long_description`` is accessed
* Documentation changes
* Removed ``demo.py``

  * Changed installation instructions to refer to **PythonTop40** on PyPI
  * Moved changes text into project route directory's ``CHANGES.RST`` and included them into ``docs/changes.rst``
  * Moved code examples out of the ``moredetail.rst`` file, and used ``literalinclude`` instead.
  * Added a link to the ReadTheDocs documentation into the README.rst file

v0.1.0.dev3 - 6th December 2014
-------------------------------
* Minor change to documentation

**ToDo** Modify links to PyPI and ReadTheDocs in the rest of the documentation.


v0.1.0.dev2 - 6th December 2014
-------------------------------
* Test coverage increased
* Initial documentation complete
* Documentation uploaded to `ReadTheDocs <http://pythontop40.readthedocs.org/en/latest/changes.html>`_
* **PythonTop40** now installable using pip - ``pip install pythontop40``
* **PythonTop40** now uploaded to `PyPi <https://pypi.python.org/pypi/pythontop40>`_

**ToDo** Modify links to PyPI and ReadTheDocs in the rest of the documentation.

V0.1.0.dev1 - 4th December 2014
-------------------------------

Initial version with working code and some tests.

**ToDo**:

* Complete tests coverage
* Complete documentation
* Upload documentation to ``readthedocs``.
* Make code installable using ``setup.py`` / ``pip``.
* Make code installable from ``PyPI`` using ``pip``.
