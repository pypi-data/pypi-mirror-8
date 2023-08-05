.. image:: https://secure.travis-ci.org/fngaha/bobtemplates.fon.png
    :target: http://travis-ci.org/#!/fngaha/bobtemplatesfon

Introduction
============

``bobtemplates.fon`` provides `mr.bob`_ templates to generate packages for
Plone projects.

Available templates are:

* `Plone`_, `Plone_nested`_: templates for a full featured Plone add-on, including:

  * zc.buildout
  * GenericSetup install profile
  * Zope 3 browser layer
  * `z3c.jbot`_ overrides folder
  * ``static/`` resourceDirectory for serving static resources (images, CSS,
    JS, etc.)
  * `Sphinx`_ documentation
  * test suite with test coverage
  * `Travis CI`_ integration


Global settings
---------------

Some answers to bob's questions can be pre-filled based on global configuration
so you don't have to answer them every time. You can store this configuration
either on you local computer, or if you are working in a team, somewhere
online.


Creating a Plone add-on package
-------------------------------

To create a Plone add-on first install ``mr.bob`` and
the ``bobtemplates.fon`` package and then run `mrbob`::

    $ pip install mr.bob
    $ pip install bobtemplates.fon
    $ mrbob --config ~/.mrbob.ini -O collective.foo bobtemplates:plone

Then answer some questions::

    --> Name of the package: foo
    (namespace is already set in the ~/.mrbob.ini)

    ...

And your package is ready!


.. _mr.bob: http://mrbob.readthedocs.org/en/latest/
.. _Plone: http://plone.org
.. _Plone_nested: http://plone.org
.. _z3c.jbot: http://pypi.python.org/pypi/z3c.jbot
.. _Sphinx: http://sphinx-doc.org/
.. _Travis CI: http://travis-ci.org/
