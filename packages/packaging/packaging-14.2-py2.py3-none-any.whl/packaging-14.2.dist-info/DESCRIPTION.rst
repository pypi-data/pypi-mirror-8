packaging
=========

Core utilities for Python packages


Discussion
----------

If you run into bugs, you can file them in our `issue tracker`_.

You can also join ``#pypa`` on Freenode to ask questions or get involved.


.. _`documentation`: https://packaging.pypa.io/
.. _`issue tracker`: https://github.com/pypa/packaging/issues

Changelog
=========


14.2 - 2014-09-10
~~~~~~~~~~~~~~~~~

* Add prerelease support to ``Specifier``.
* Remove the ability to do ``item in Specifier()`` and replace it with
  ``Specifier().contains(item)`` in order to allow flags that signal if a
  prerelease should be accepted or not.
* Add a method ``Specifier().filter()`` which will take an iterable and returns
  an iterable with items that do not match the specifier filtered out.


14.1 - 2014-09-08
~~~~~~~~~~~~~~~~~

* Allow ``LegacyVersion`` and ``Version`` to be sorted together.
* Add ``packaging.version.parse()`` to enable easily parsing a version string
  as either a ``Version`` or a ``LegacyVersion`` depending on it's PEP 440
  validity.


14.0 - 2014-09-05
~~~~~~~~~~~~~~~~~

* Initial release.


