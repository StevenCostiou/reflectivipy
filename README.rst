=====================================================================================
Reflectivity: A Python Implementation of the Reflectivity API from the Pharo language
=====================================================================================

Reflectivipy is an API inspired by `Reflectivity in Pharo
<http://scg.unibe.ch/research/reflectivity>`_. Reflectivity allows you to deal
with partial behavioral reflection in Python by letting you install ``MetaLink``
directly on method AST nodes. Moreover, Reflectivity provides object-centric
capabilities and let you install a modified behavior on a dedicated object.

Let see how to install a link on a method AST towards a meta-object:

.. code-block:: python

    import reflectivipy


    # We define a new meta-object that will act as a logger
    # each time a dedicated AST node will be "visited/executed"
    class MetaLogger(object):
      def log_me(self):
        print "I'm here"


    # Here is the class we will instrument
    class ExampleClass(object):
      def foo(self):
        print 'Executing foo'


    # We create a link ('control' is 'before' by default)
    link = reflectivipy.MetaLink(MetaLogger(), selector='log_me', control='before')

    # We get the method AST we want to instrument
    rf_ast = reflectivipy.reflective_ast_for_method(ExampleClass, 'foo')

    # We select the node that we want to install the link on
    # Here we selected the "print 'Executing foo'" AST node.
    node = rf_ast.body[0].body[0]

    # We install the link on the node
    reflectivipy.link(link, node)

    a = ExampleClass()
    a.foo()

    # When we don't need it anymore, we remove it
    print 'Uninstall Metalink'
    link.uninstall()

    a.foo()

    # Produces:
    #
    # I'm here
    # Executing foo
    # Uninstall Metalink
    # Executing foo


This small code example uses the two main Reflectivipy concepts:

- the meta-object definition, i.e: the object that will own the behavior to add
- the ``MetaLink`` in itself which link the meta-object to the AST node that
  must be modified.

The MetaLink ``link`` is used to install a new behavior ``before`` the code
associated  to the AST node on which it will be installed. The method AST is
then gathered using the ``reflective_ast_for_method`` function. The desired AST
node is gathered (here it's the ``print`` node). Finally, the node and the
meta-behavior are linked together using the ``link`` function. Once the new
meta-behavior is not required anymore, the ``uninstall`` method of the created
link is called. This call uninstall the link from every node it could be
installed on.

On top of that, meta-behavior can be installed for a dedicated instance instead
of a class. To do that, it's just a matter of asking for the
``reflective_ast_for_method`` of the instance instead of the one from the class.
The code remains then exactly the same.


Installation
============

Currently, Reflectivity is not yet on ``pypi``, so you can install it using
``pip``. It is recommanded to install it in the virtualenv.

.. code-block:: bash
    $ pip install -e .


Quick Start
===========


Contributors
============

* Steven Costiou (`@StevenCostiou <https://github.com/StevenCostiou>`_), main author of Reflectivipy
* Vincent Aranega (`@aranega <https://github.com/aranega>`_)
