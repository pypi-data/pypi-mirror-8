django-conversejs
=================

This app aims to make easier to integrate `Converse.js`_ into Django.

Currently ``django-conversejs`` provides:

* A minified distribution of converse.js
* Template tags to help you to include converse.js on your Django project
* A database model to store the XMPP user and password for each user
* Converse.js configurations through settings.py
* Single-sign-on (SSO) like experience


.. _Converse.js: http://conversejs.org/


Installing and configuring
---------------------------


Install SleekXMPP from ``TracyWebTech/fix-gevent`` branch:

::

    pip install git+https://github.com/TracyWebTech/SleekXMPP@fix-gevent

Install django-conversejs:

::

    pip install git+https://github.com/TracyWebTech/django-conversejs

Add ``conversejs`` to installed apps in your settings.py:

.. code-block:: python

    INSTALLED_APPS = {
        ...
        'conversejs',
        ...
    }

Configure the BOSH service URL in your settings.py:

.. code-block:: python

    CONVERSEJS_BOSH_SERVICE_URL = 'https://my-bosh-service.com'

Load the static files in your templates using django-conversejs custom tags:

.. code-block:: html+django

    {% load conversejs %}
    ...
    <head>
      ...
      {% conversejs_static %}
      ...
    </head>

Load the chat panel and the Javascript initilizalizer also using our custom tags:

.. code-block:: html+django

    {% load conversejs %}
    ...

      {% conversejs_chatpanel %}
      {% conversejs_initialize %}
    </body>

Update database schema:

::

    python manage.py syncdb
    python manage.py migrate # optional


Adding an XMPP account
----------------------

* Log in the Django Admin

* Add an XMPP account by clicking in the '+ Add' button

* Choose the user from the select box and them type the JabberID and password for the account

Now everytime the select user your logs in your site he will be automatically logged in the XMPP
server using the credentials you provided.


Enabling XMPP auto registration
--------------------------------

By enabling auto registration ``django-conversejs`` will attempt to create a new
XMPP account for every user that doesn't have one as soon as they login in your site.

To enable you just need to add the ``CONVERSEJS_AUTO_REGISTER`` option to your
settings.py setting it to the domain of your XMPP service. Notice that the XMPP
server and the BOSH service URL are two different things.

For example:

.. code-block:: python

    CONVERSEJS_BOSH_SERVICE_URL = 'https://my-bosh-service.com'

    CONVERSEJS_AUTO_REGISTER = 'xmpp.mycompany.com'


In the example above Django will get the username from ``request.user.username`` and
try to register under the xmpp domain ``xmpp.mycompany.com``, so if an user john logs in it would try to register ``john@xmpp.mycompany.com``.

If registration fails for any reason ``django-conversejs`` will attempt again on every request. That's something to be improved.


Forms
------

If you want to create custom forms to keep the look and feel of your site you can use
conversejs.forms as a start point.


Converse.js Version
-------------------

We currently ship Converse.js **v0.6.4 (patched)**.

If you need a newer version, please open an issue or a pull request.


TODO
----

* Write tests
* Allow user reset XMPP account password. That's useful to allow the use of other xmpp clients.
* Allow user to set avatar
* Auto update XMPP name and email when those are updated in django (using signals)
