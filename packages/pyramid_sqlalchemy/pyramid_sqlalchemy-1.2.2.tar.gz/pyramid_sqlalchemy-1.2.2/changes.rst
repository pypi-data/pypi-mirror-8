Changelog
=========

1.2.2 - September 11, 2014
--------------------------

- Add dependency on mock for Python <3.3. This fixes import problems who try to
  import pyramid_sqlalchemy.testing in production code.


1.2.1 - September 1, 2014
-------------------------

- Move pyramid to a test-only dependency. This makes it simpler to use
  pyramid_sqlalchemy in non-pyramid contexts.


1.2 - August 30, 2014
---------------------

- Use `unittest.mock` when available. This removes the `mock` dependency on
  Python 3.

- Tests no longer need to mock out pyramid_sqlalchemy.includeme; this is now
  handled by ``DatabaseTestCase`` and the py.test fixtures.

- Automatically make py.test fixtures available externally. This removes the
  need to copy & paste them over from the documentation.

- Fix error on pytest fixture example.

- Setup `Travis <https://travis-ci.org/wichert/pyramid_sqlalchemy>`_ to
  automatically run tests on CPython 2.6, CPython 2.7, CPython 3.3, CPython 3.4
  and PyPy.


1.1 - July 14, 2014
-------------------

- Add missing schema to the Pyramid-URL in the package description. This broke
  ReST rendering on the PyPI page.

- Add a new ``enable_sql_two_phase_commit()`` configuration directive to enable
  two-phase commit.

- Enable foreign key constraint checking for SQLite in DatabaseTestCase.

- Use SQLAlchemy events instead of ZopeTransactionExtension to handle
  integration of zope.sqlalchemy and SQLAlchemy.


1.0 - July 13, 2014
-------------------

- First release.
