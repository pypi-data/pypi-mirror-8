=======
CHANGES
=======

4.1.0 (2014-12-24)
==================

- Added support for PyPy.  PyPy3 support is pending a release of fix for
  https://bitbucket.org/pypy/pypy/issue/1946).

- Added support for Python 3.4.

- Support for testing on Travis.


4.1.0a1 (2013-02-22)
====================

- Added support for Python 3.3.


4.0.0 (2012-07-04)
==================

- Strip noise from context actions in doctests.

  The output is now more meaningful, and hides irrelevant details.
  (forward-compatibility with ``zope.component`` 4.0.0).

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.4 and 2.5.


3.9.1 (2010-04-30)
==================

- Removed use of 'zope.testing.doctestunit' in favor of stdlib's 'doctest.

3.9.0 (2009-08-27)
==================

Initial release. This package was splitted off zope.app.publisher.
