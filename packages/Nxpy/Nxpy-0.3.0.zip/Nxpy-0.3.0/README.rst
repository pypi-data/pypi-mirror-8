Nick's Python Toolchest - 0.3.0
===============================

Nxpy is an etherogeneous collection of useful modules, dealing with diverse topics such as 
wrapping complex commands with API's or interacting with Java and .NET build systems. 
There are also more basic utilities, such as automation of backup files, support for writing your 
own file-like objects and many other things.

The library is being developed with Python 3.4 so as to be compatible with Python 2.7. Most modules
should work also with 2.6, 3.2 and 3.3. Some still work with 2.5.

The only enforced dependency is `six <http://pythonhosted.org/six/>`_. On Windows 
`pywin32 <https://pypi.python.org/pypi/pywin32>`_ is required, but not enforced. Some packages have
specific dependencies of their own:

 * :py:mod:`.ply` requires `PLY <http://www.dabeaz.com/ply/>`_;
 * :py:mod:`.scons` requires `SCons <http://www.scons.org/>`_;
 * :py:mod:`.wx` requires `wxPython <http://wxpython.org/>`_.
 