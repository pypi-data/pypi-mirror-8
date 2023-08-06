Installation Instructions
=========================

First step
----------

If you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can add ``collective.lineage``
to your instance part::

    [instance]
    ...
    eggs =
      Plone
      collective.lineage
    # the next 2 lines are not necessary
    # if you are using lineage-0.6+
    zcml =
      collective.lineage


If you are using Plone 3.2
---------------------------

You will need to use the code added for `PLIP 234`.
To do so, you'll have to add the branches of the eggs for the plip::

    [buildout]
    parts =
      ...
      plip234-branches
    
    [plip234-branches]
    recipe = infrae.subversion
    as_eggs = true
    urls =
      http://svn.plone.org/svn/plone/Plone/branches/calvinhp-inavigationroot-fixes Plone
      http://svn.plone.org/svn/plone/plone.app.layout/branches/calvinhp-inavigationroot-fixes plone.app.layout
      http://svn.plone.org/svn/plone/plone.app.portlets/branches/calvinhp-inavigationroot-fixes plone.app.portlets

If you are using Plone 3.1.7
----------------------------

You will need to use the branches created by duffyd (note the reference
to ``${plone317-products:location}`` in the ``products`` value of the
``instance`` section must be first in the list)::

    [buildout]
    parts =
    ...
    plone317-products
    plone317-eggs
    
    [instance]
    recipe = plone.recipe.zope2instance
    ...
    products =
        ${plone317-products:location}
        ...
    
    [plone317-products]
    recipe = infrae.subversion
    urls =
        http://svn.plone.org/svn/plone/Plone/branches/duffyd-inavigationroot-fixes-317/ Plone
    
    [plone317-eggs]
    recipe = infrae.subversion
    as_eggs = true
    urls =
        http://svn.plone.org/svn/plone/plone.app.layout/branches/duffyd-inavigationroot-fixes-317/ plone.app.layout
        http://svn.plone.org/svn/plone/plone.app.portlets/branches/duffyd-inavigationroot-fixes-317/ plone.app.portlets


Last step
---------

Now you can re-run your buildout to get the all the dependencies::

    $ bin/buildout

Once your buildout is finished, you can start up your instance and
install Lineage via the ``Add-on Products`` configlet in site setup.

.. _PLIP 234: http://plone.org/products/plone/roadmap/234

Migration from 0.1 to the latest version
========================================

In versions of collective.lineage that are greater than 0.1, the Child
Folder type has been deprecated and you can know activate a folder using
the subtyper action when you are on a Folder.

An upgrade step takes care of migrating the old Child Folder to Folder.
Make sure to backup your data and then, once you have updated your
instance to use the latest collective.lineage, reinstall "Lineage", it
will migrate the items automatically.

NOTE: we are assuming that the Child Folder and the Folder workflows are
the same.

Migration to 1.0
================

Pre-1.0 installations will need to run the GenericSetup profile when
migrating to 1.0 or your site will produce a ``SiteError`` when
attempting to view because of the changes that have been made. Please
login to the ZMI and go to the ``portal_setup`` tool and select the
``Lineage`` profile from the import tab and run all steps. You site will
be ready to go.

Working on the trunk of lineage
===============================

To work on the trunk of lineage, do the following::

    $ svn co https://svn.plone.org/svn/collective/collective.lineage/trunk/ lineage-trunk
    $ cd lineage-trunk
    $ python2.4 bootstrap.py
    $ bin/buildout -v
    $ bin/instance fg

Then:

- go to  http://localhost:8080/manage (admin/admin)
- add a plone site
- quickinstall lineage in the new plone site
- create a folder and subtype it to see if everything works fine 

You can run the tests in debug mode with the following command::

    $ bin/test -D

