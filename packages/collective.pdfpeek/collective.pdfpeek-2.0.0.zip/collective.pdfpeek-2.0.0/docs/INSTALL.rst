Installation
============

Via zc.buildout
---------------

The recommended method of using collective.pdfpeek is by installing via
zc.buildout using the plone.recipe.zope2instance recipe.
PdfPeek uses z3c.autoinclude to load it's zcml, so you don't need a zcml slug.

Add collective.pdfpeek to the list of eggs in the instance section of your
buildout.cfg like so::

    [instance]
    ...
    eggs =
        ...
        collective.pdfpeek
        ...

Then re-run your buildout like so to activate the installation::

   $ bin/buildout

Via setuptools
--------------

To install collective.pdfpeek into the global Python environment (or a virtualenv),
using a traditional Zope 2 instance, you can do this:

* When you're reading this you have probably already run
  ``easy_install collective.pdfpeek``. Find out how to install setuptools
  (and EasyInstall) here:
  http://peak.telecommunity.com/DevCenter/EasyInstall

* If you are using Zope 2.9 (not 2.10), get `pythonproducts`_ and install it
  via::

    python setup.py install --home /path/to/instance

into your Zope instance.

* Create a file called ``collective.pdfpeek-configure.zcml`` in the
  ``/path/to/instance/etc/package-includes`` directory.  The file
  should only contain this::

    <include package="collective.pdfpeek" />

.. _pythonproducts: http://plone.org/products/pythonproducts


Configuration
=============


Via zc.buildout
---------------

For automatic processing of the PdfPeek job queue, a simple cron script using
curl or wget would suffice. It is nice to keep all of the configuration for a
project in your buildout, however. For this reason, a zope clock server process
is the recommended way to automatically process the job queue. You can do so by
adding the following snippet to your [instance] part in your buildout
configuration::

    [instance]
    ...
    zope-conf-additional=
        # process the job queue every 5 seconds
        <clock-server>
           method /Plone/@@pdfpeek.utils/process_conversion_queue
           period 5
           user admin
           password admin
           host localhost
        </clock-server>
    ...

You will have to edit the above snippet to customize the name of the plone site,
the admin username and password, and the hostname the instance is running on.
You can also adjust the interval at which the queue is processed by the clock
server.

Then re-run your buildout like so to activate the clock server::

   $ bin/buildout


Via cron
--------

Install ``wget``. \

Edit your crontab file and append the following line::

     5 * * * * wget --user=admin --password=admin http://localhost:8080/Plone/@@pdfpeek.utils/process_conversion_queue

You will have to customize the above line with the hostname, port number, username, password and path to your plone instance.

Save your crontab file and wget will now call the view method that triggers the
processing of the pdf conversion queue every five minutes.


Via RabbitMQ
------------

Install rabbitmq-server on your machine. There are very good documentations
on the rabbitmq website, see: http://www.rabbitmq.com/download.html

Instead of configuring a clockserver, you should configure collective.zamqp to
work, see following example::

    [buildout]
    parts =
        instance
        worker

    ...

    [instance]
    recipe = plone.recipe.zope2instance
    http-address = 8080
    eggs =
        ...
        collective.pdfpeek [zamqp]

    ...
    zope-conf-additional =
        %import collective.zamqp
        <amqp-broker-connection>
            connection_id   superuser
            hostname        my.rabbithostname.com
            port            5672
            username        guest
            password        guest
            heartbeat       120
            keepalive       60
        </amqp-broker-connection>

    [worker]
    <= instance
    http-address = 8081
    zserver-threads = 1
    environment-vars =
        ZAMQP_LOGLEVEL INFO
    zope-conf-additional =
        ${instance:zope-conf-additional}
        <amqp-consuming-server>
            connection_id   superuser
            site_id         Plone
            user_id         admin
        </amqp-consuming-server>

For advanced configuration see ``collective.zamqp`` documentation here:
https://pypi.python.org/pypi/collective.zamqp
