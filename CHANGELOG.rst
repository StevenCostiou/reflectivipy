Changelog
---------

0.1.0
+++++

**Features**

- Add support for Python 3.


0.0.2
+++++

**Features**

- Add support for ``instead`` control for metalinks. This new control allows the
  user to remove a node and to place a meta-behavior instead. The new behavior
  can be uninstall using the ``uninstall()`` method on the link.

- Add support for decorators. This new implementation search for the function at the
  most "lower" level for methods and gets the function pointed by the decorators.

- Add support for modules. This new implementation is able to install metalinks
  on function at a module level.


0.0.1
+++++

**Initial version**
