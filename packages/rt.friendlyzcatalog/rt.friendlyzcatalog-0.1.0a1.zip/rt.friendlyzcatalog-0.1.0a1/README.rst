Introduction
============

The ZCatalog tool (and the Plone CatalogTool version) has a very old user interface
with some limitation, and also some annoying behavior.

Although using ZMI catalog UI for complex task is not good, sometimes you need it.

.. Note::
    This is a really experimental package.
    **You at your how risk**

New features
============

Page size
---------

The "*Catalog"* view display the whole catalog (or selection result) using a batching
of 20 items.
You can now use an higher value.

Command "*Quick Update Catalog*"
--------------------------------

In the "*Advanced*" view you can now use the new "*Quick Update Catalog*" button.
It will *not* clear the catalog before reindexing, and it will skip indexing on
"slow" index (right not: only ``ZCTextIndex``) is skipped.

So: after this call you catalog *can* contain old data in text indexes, but the reindex
will be a lot quicker (expecially on sites where you indexes file contents).

Obviously, if you nead a good cleanup, just use the default "*Update catalog*"

Safer unindex
-------------

Sometimes a catalog index enter in a broken state where it have no reference about an
indexed object. The ``uncatalogObject`` can fail just because a single index has no reference
about an object.

The change will swallow this kind of errors (a log entry will be displayed) but the unindex
operation will goes on.

Zope and Plone versions
=======================

Tested on Plone 4.3 (and ZCatalog version distributed with it).

Why you don't provide those changes to Zope core?
=================================================

That's a long story and sad story.

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
