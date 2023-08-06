====================
rg.infocard
====================

.. contents::

Resources
=========

* `Source code @ GitHub <https://github.com/PloneGov-IT/rg.infocard>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/rg.infocard>`_

How it works
============

This product introduces two new content types to your Plone site:

- `Infocard container`
- `Infocard`

Infocard container
------------------

This content type is supposed to contain infocards.

Beside normal Plone content fields (title, description, rich text),
it has some configurable parameters to define:

- Service types
- Recipients
- A template for the contained infocard

It's default view is a form to search inside the contained infocards.

Infocard
--------

An infocard is a content with a tabular field
(whose default values can be specified in the infocard container).
The Infocard records at each save the modifier.

Using rg.infocard
=====================

Create a new infocard container
-------------------------------

Once the product is installed, the **Infocardcontainer** entry
will be available on the ``Add new`` action menu.
Click on it to add a new **Infocardcontainer**.

.. image:: http://blog.redturtle.it/pypi-images/rg.infocard/add-infocardcontainer.png/image_preview
  :alt: The add view of the Infocard container
  :target: http://blog.redturtle.it/pypi-images/rg.infocard/add-infocardcontainer.png

Creating a new infocard
-----------------------

In the view of an infocard container it is possible to add,
from the ``Add new`` menu,
a new Infocard.

.. image:: http://blog.redturtle.it/pypi-images/rg.infocard/add-infocard.png/image_preview
  :alt: Link to create new entry
  :target: http://blog.redturtle.it/pypi-images/rg.infocard/add-infocard.png

The available options
for the service types and recipients fields
are controlled by the homonymous fields of the container.

Changing service types and recipients fields on the container **has effect** on

The Informations datagrid default to the value of
the homonymous fields of the container.

Changing the service types and recipients fields on the container
**has effect** on the already created infocards.

Changing the informations field on the container
**has no effect** on the already created infocards.

Table lines
-----------

Each table line accept the following parameters:

- label
- value
- public

Label will contain a text line descriptive of the value

Value is accepts simple text or html markup
(click on the pencil icon to activate TinyMCE editor).

Public is a checkbox (by default it is unchecked).
If checked the line will be displayed in the view of a public Infocard.

Table lines can be added, removed or sorted clicking
on the buttons at the right.


Installation
============

To install **rg.infocard** you simply add **rg.infocard**
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install **rg.infocard** using the Add-ons control panel.

Credits
=======

Developed with the support of:

* `Unione Reno Galliera`__

  .. image:: http://blog.redturtle.it/pypi-images/rg.prenotazioni/logo-urg.jpg/image_mini
     :alt: Logo Unione Reno Galliera

Unione Reno Galliera supports the `PloneGov initiative`__.

__ http://www.renogalliera.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
