====================
collective.superfish
====================

.. contents::

What is it?
===========

collective.superfish integrates the `jQuery Superfish plugin`_ into Plone.

Superfish is a really nice solution for dropdown menus using css, valid xhtml
and JavaScript which degrades gracefully if JavaScript is not available.

.. _`jQuery Superfish plugin`: http://users.tpg.com.au/j_birch/plugins/superfish/


.. ATTENTION::

    Dropdown currently does not work on iOS devices.
    The `hoverintent.js` requires jQuery 1.9.1+ and Plone 4.3.3 ships with 1.7.2

    see https://github.com/collective/collective.superfish/issues/1 for
    workarounds or use 0.X releases

How do i use it?
================

Hide `plone.global_sections` and replace it with `collective.superfish`
in viewlets.xml somehow like this::

    <!-- superfish: use superfish instead of global_sections -->
    <hidden manager="plone.portalheader" skinname="MySkin">
        <viewlet name="plone.global_sections" />
    </hidden>

    <order manager="plone.portalheader" skinname="MySkin">
        <viewlet name="collective.superfish" insert-after="plone.global_sections" />
    </order>


Customization
=============


Add portal_actions
------------------

By default, `collecive.superfish` does not include portal_actions in the menu.
To activate them, subclass the viewlet::

    from collective.superfish.browser.sections import SuperFishViewlet as SuperFishBase

    class SuperFishViewlet(SuperFishBase):

        ADD_PORTAL_TABS = True

and register it for your skin::

    <browser:viewlet
        name="collective.superfish"
        manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
        class=".viewlets.SuperFishViewlet"
        permission="zope2.View"
        layer=".interfaces.IThemeSpecific"/>


Do not show arrows
------------------

To not show the arrows for menuitems with subitems,
customize the Javascript initialization::


    jQuery('ul.sf-menu').superfish({
        cssArrows: false
    });

See http://users.tpg.com.au/j_birch/plugins/superfish/options/ for a complete
list of available options.


CSS Styles
----------

By using superfish.css you should have everyting in place to get a working
superfish navigation.

Specific fixes and colors for plone's `Sunburst Theme` can be found in
superfish-plone.css (you might deactivate these styles for your custom theme
layer to not need to override these styles)

You might want to have a look at the examples provided in the
`superfish download <https://github.com/joeldbirch/superfish/archive/1.7.4.zip>`_

eg: https://github.com/joeldbirch/superfish/tree/1.7.4/examples


