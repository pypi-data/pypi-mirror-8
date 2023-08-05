.. contents::

Introduction
============

Add custom views to the Plone booking product `pd.prenotazioni`__.

__ https://pypi.python.org/pypi/pd.prenotazioni

The functionality of this package will be merged in
`pd.prenotazioni`__.

__ https://pypi.python.org/pypi/pd.prenotazioni


The views
=========

prenotazione_add_ro
-------------------

This is a form with all fields hidden.
It is meant to be used to display the data before final submission.

slots.json
----------

Call this view like this:

- http://localhost:8080/Plone/agenda/slots.json?booking_date=2014/06/23

It will return a list of urls::

    [
        "http://localhost:8080/Plone/agenda/prenotazione_add?form.booking_date=2014-06-23+09%3A00&",
        "http://localhost:8080/Plone/agenda/prenotazione_add?form.booking_date=2014-06-23+09%3A05&",
        ...
        "http://localhost:8080/Plone/agenda/prenotazione_add?form.booking_date=2014-06-23+17%3A50&",
        "http://localhost:8080/Plone/agenda/prenotazione_add?form.booking_date=2014-06-23+17%3A55&"
    ]

If the parameter ``booking_date`` is not specified it will default to today.


tipologies.json
---------------

Call this view like this:

- http://localhost:8080/Plone/agenda/@@tipologies.json

It will return a json object::

    {
        "Task for 1 person": 10,
        "Task for 2 people": 20,
        "Task for 3 people": 30
     }

The key is the booking tipology name,
the value the booking duration in minutes.

Credits
=======

Developed with the support of `Comune di Padova`__.

Comune di Padova supports the `PloneGov initiative`__.

.. image:: https://raw.githubusercontent.com/PloneGov-IT/pd.prenotazioni/master/docs/logo-comune-pd-150x200.jpg
   :alt: Comune di Padova's logo

__ http://www.padovanet.it/
__ http://www.plonegov.it/


Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
      :target: http://www.redturtle.it/