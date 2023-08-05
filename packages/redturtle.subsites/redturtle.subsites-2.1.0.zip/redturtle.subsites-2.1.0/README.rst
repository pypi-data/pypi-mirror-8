.. contents::

Introduction
============

This subsite product add to Plone some minimalistic **subsite** feature.

Before installing
-----------------

This product try to perform the task adding minimal code to Plone but also need that part of the work
will be done by other software, in that case `Apache`__.

__ http://en.wikipedia.org/wiki/Apache_HTTP_Server 

So, if you are looking for a complete and self-contained subsite product for Plone, let try other products (like
`Lineage`__) before this.

__ http://pypi.python.org/pypi/collective.lineage/

What is a subsite ?
-------------------

In this document **a subsite is a section of your Plone site** that:

* need (commonly) a different theme applied
* the visitor surf the subsite accessing something like *domain.com/subsite*, *subsite.com*
  or *subdomain.domain.com*
* the visitor can be not aware that he's visiting a subsection of a bigger site
* site contributors (commonly) access the site through a *back-end.domain.com* domain
* site contributors (can) see a different Plone theme
* site contributors (commonly) see the whole site, not only the subsite (as far as they use the back-end URL)

Note that this approach is not limited to a single subsite, but you can have more than once. All subsites are
edited using a **back-end URL**, then visited using some **front-end URLs**

Note also that you can continue having front-end contributors, but they are limited to the subsite when move
in and out of folders, using TinyMCE, and so on. Again, they could not know that are inside Plone subsite.

You really need a subsite?
--------------------------

If you *dont'* need a Plone site where...

* you can create an internal link to a content inside another subsite
* you can create a collection that take contents from more that a subsite
* when you use the site search, you want to find also documents outside the subsite

...probably you *don't need a subsite* but simply need a Zope instance with multiple Plone site inside it!

But if one of the behavior above are true, keep reading.

Subsite sometimes is only matter of theme
-----------------------------------------

If the concept of subsite inside your organization don't require "isolation" (of navigation, of breadcrumb,
portal tabs, TinyMCE use, ...) probably you only need the Apache + Plone magic described there, not this
(or other) subsite product.

Create a subsite Plone theme
============================

As already noted, this product will do pretty much anything without Apache in front of Plone, and you'll need
to customize your Apache rewrite rules.

All is based on some behavior already inside Plone, like the power to apply a Plone theme adding an HTTP header
that Plone will handle in a special way.

Also you will play no more with the Plone "*Default theme*" option under the "*Theme settings*" site setup section,
or simply you will use this option only for the back-end theme.

A full example available
------------------------

We also provide a full `Plone subsite example theme`__, that use all that follow.

__ http://pypi.python.org/pypi/example.rtsubsites_theme

The theme's interface
---------------------

You need to create (or customize) the Plone theme that you want to apply to the subsite. Please **note** that
even if you don't plan to see a different theme for the front-end, you still need to create an empty theme.

Commonly this theme must be installed in your Plone site, but it must not register himself as Plone default theme
(so don't use the ``default_skin=xxx`` attribute in your skins.xml Generic Setup file).

The only important part of the theme is the interface declaration.
Commonly Plone themes have a file like ``plone_theme.mysite/plone_theme/mysite/browser/interfaces.py``.

The file looks like this:

.. code-block:: python

    from plone.theme.interfaces import IDefaultPloneLayer
    
    class IThemeSpecific(IDefaultPloneLayer):
        """Marker interface that defines a Zope 3 browser layer.
        """

You need to change the interface as follow:

.. code-block:: python

    from redturtle.subsites.frontend.browser import IFrontendLayer
    
    class IThemeSpecific(IFrontendLayer):
        """Marker interface that defines a Zope 3 browser layer.
        """

See also https://github.com/RedTurtle/example.rtsubsites_theme/blob/master/example/rtsubsites_theme/browser/interfaces.py

Other theme's components
------------------------

After previous step you can continue adding element (JavaScript files, CSS, images, templates) normally. If you
don't need that the new theme doesn't looks like the default site theme, you theme is already finished.

Logo viewlet
------------

The logo viewlet provided with the product is customized, to take always the default logo from the subsite URL.

If you need to customize the logo viewlet in your theme, please think about extend the redturtle.subsites ones:

.. code-block:: python


    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    from redturtle.subsites.frontend.viewlets.logo import LogoViewlet as BaseLogoViewlet
     
    class LogoViewlet(BaseLogoViewlet):
         # do something here

See also https://github.com/RedTurtle/example.rtsubsites_theme/blob/master/example/rtsubsites_theme/browser/logo.py

Remember: you need to perform this task only if you need to customize the logo viewlet.

Mark a Plone Folder as a Subsite
================================

The first and only Plone task for obtain a subsite is to choose a Folder that must be the subsite.

Go to the folder through ZMI and apply a new additional marker interface.
From the "*Interfaces*" tab find the ``redturtle.subsites.backend.interfaces.ISubsiteRoot`` from the
"Available Marker Interfaces" section and add it.

You can remove the marker from this same page.

Apply the theme (AKA get a Subsite)
===================================

We will show now what to add to your Apache configuration and transform all this in the subsite environment
we need.

RequestHeader
-------------

Starting from redturtle.subsites 2.1 whay our need is simple a `RequestHeader`__ additional configuration.

__ http://httpd.apache.org/docs/2.0/mod/mod_headers.html#requestheader

Note that this only works if the ``request_varname`` of ``portal_skins`` tool will be changed from ``plone_skin`` to
``HTTP_PLONE_SKIN``. You can do this manually from ZMI (*REQUEST variable name* field) or through Generic Setup
(see
https://github.com/RedTurtle/example.rtsubsites_theme/blob/master/example/rtsubsites_theme/profiles/default/skins.xml
).

You need to write something like this::

    RequestHeader append plone_skin "The name of the Theme"

Different domain (or subdomain) how-to
--------------------------------------

When your subsite domain is something like *subsite.com* (or *subdomain.mycompany.com*) the configuration is quite
simple. You will provide to your Apache a ``subsite.com.conf`` file with something like this inside::

    <VirtualHost host:80>
        ServerName subsite.com
        ServerAlias www.subsite.com
        ServerAdmin ...

        ...

        RewriteEngine On

        RequestHeader append plone_skin "The name of the Theme"

        RewriteRule ^/(.*) \
        "http://127.0.0.1:8080/VirtualHostBase/http/%{SERVER_NAME}:80/Plone/VirtualHostRoot/subsite/$1" [L,P]
        ProxyPassReverse / http://127.0.0.1:8080/
        
        ...
        
    </VirtualHost>

Subsite inside a subpath how-to
-------------------------------

If you already have a Plone site at mycompany.com, and visiting http://mycompany.com/subsite you need a subsite,
the configuration is complex because you need to handle both in the same ``.conf`` file::

    <VirtualHost host:80>
        ServerName mycompany.com
        ServerAlias www.mycompany.com
        ServerAdmin ...

        ...

        RewriteEngine On

        SetEnvIf Request_URI "^/subsite(.*)" SUBSITE
        RequestHeader append plone_skin "The name of the Theme" env=SUBSITE

        RewriteRule ^/(.*) \
        "http://127.0.0.1:8080/VirtualHostBase/http/%{SERVER_NAME}:80/Plone/VirtualHostRoot/$1" [L,P]
        ProxyPassReverse / http://127.0.0.1:8080/

        ...

    </VirtualHost>

Additional products
===================

If you like also to manage portal tab of your subsites in a different way that isn't the standard Plone
behavior, take a look at `collective.navroottabs`__. With this you will be able also to customize different
portal tabs for your subsites. 

__ http://plone.org/products/collective.navroottabs

Dependencies
============

Tested on Plone 4.3.

TODO
====

As we removed ``p4a.subtyper``, the subsite marker can only be given through ZMI access. This will probably
change in the future.

Credits
=======

Developed with the support of `Rete Civica Mo-Net - Comune di Modena`__;
Rete Civica Mo-Net supports the `PloneGov initiative`__.

.. image:: http://www.comune.modena.it/grafica/logoComune/logoComunexweb.jpg
   :alt: Comune di Modena - logo

__ http://www.comune.modena.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
