repoze.zcml Changelog
=====================

1.0b1 (2014-12-11)
------------------

- Added support for PyPy and PyPy3.

- Added support for Python 3.2, 3.3, 3.4.

- Added support for continuous integration using ``Travis``.

- Added support for continuous integration using ``tox`` and ``jenkins``.

- Added 'setup.py dev' alias (runs ``setup.py develop`` plus installs
  ``nose`` and ``coverage``).

0.4 (2009-09-15)
----------------

- Make ``zope.testing`` dependency a testing-only requirement.

- 100% test coverage.

0.3 (2009-05-28)
----------------

- Provide compatbility with older versions of zope.component which
  have a CA registry that doesn't accept a ``factory`` argument
  to ``registerUtility``.

0.2
---

- Depend on ``zope.component >= 3.5.0`` (utility directive requires it).

0.1
----------------

- Initial release.
