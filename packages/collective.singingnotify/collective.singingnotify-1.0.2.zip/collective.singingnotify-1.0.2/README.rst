Introduction
============
A customization for *Singing&Dancing* that sends a notify mail on subscription events.

Usage
=====
This product add two new contentrules:

- User confirm newsletter subscription
- User unsubscribed from newsletter

These rules can be applied in every folder, and there is a specific action that allows to send an email notification with some informations.

The rule should be created in *Content Rules* control panel

.. image:: http://blog.redturtle.it/pypi-images/collective.singingnotify/add_contentrule.png
   :alt: Add contentrule


After creating the new rule, you need to set the action:

.. image:: http://blog.redturtle.it/pypi-images/collective.singingnotify/unsubscribed_form.png
   :alt: Unsubscribed contentrule


If you use this product with `collective.dancefloor`__ you can set the rule in one single local newsletter, and set different messages in every local newsletter.

__ http://pypi.python.org/pypi/collective.dancefloor

Dependencies
============

This product works with `Singing&Dancing`__.

__ http://pypi.python.org/pypi/collective.dancing

This product has been tested on Plone 3.3.5 and Plone 4.2

Credits
=======

Developed with the support of `Regione Emilia Romagna`__;

Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Site
   :target: http://www.redturtle.net/
