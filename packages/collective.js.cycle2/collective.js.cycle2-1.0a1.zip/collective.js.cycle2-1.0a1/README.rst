********************
collective.js.cycle2
********************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

`Cycle2`_ is a versatile slideshow plugin for jQuery built around ease-of-use.
It supports a declarative initialization style that allows full customization without any scripting.
Simply include the plugin, declare your markup, and Cycle2 does the rest.

.. _`Cycle2`: http://jquery.malsup.com/cycle2/

Mostly Harmless
===============

.. image:: https://secure.travis-ci.org/collective/collective.js.cycle2.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/collective.js.cycle2

.. image:: https://coveralls.io/repos/collective/collective.js.cycle2/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/collective.js.cycle2

.. image:: https://pypip.in/d/collective.js.cycle2/badge.png
    :alt: Downloads
    :target: https://pypi.python.org/pypi/collective.js.cycle2

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.js.cycle2

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.js.cycle2`` and click the 'Activate' button.

.. Note::

    You may have to empty your browser cache and save your resource registries in order to see the effects of the product installation.

Functional Plugins
------------------

The package also install the following Cycle2 functional plugins:

Center
    Support for centering slides horizontally and vertically within the slideshow container.
    You can do this easily yourself with fixed-size slideshows and simple CSS.
    This plugin makes life simpler when your slideshow has a fluid width or height.

Swipe
    If you want swipe events and you're not using jQuery Mobile, use this plugin.
    This plugin provides support for advancing slides forward or back using a swipe gesture on touch devices.

Not entirely unlike
===================

`collective.js.galleria`_
    Galleria is a JavaScript image gallery framework built on top of the jQuery library.
    The aim is to simplify the process of creating professional image galleries for the web and mobile devices.

.. _`collective.js.galleria`: https://pypi.python.org/pypi/collective.js.galleria
