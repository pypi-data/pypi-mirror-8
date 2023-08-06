..  image:: https://travis-ci.org/collective/collective.pdfpeek.png?branch=master
    :target: https://travis-ci.org/collective/collective.pdfpeek

..  image:: https://coveralls.io/repos/collective/collective.pdfpeek/badge.png
    :target: https://coveralls.io/r/collective/collective.pdfpeek

Introduction
============

PdfPeek is a Plone 4 add-on product that utilizes GNU Ghostscript to generate
image thumbnail previews of PDF files uploaded to ATFile based content
objects. Dexterity (and ``plone.app.contenttypes``) support was added in
``2.0.0`

* This product, when installed in a Plone 4.x site, will automatically generate
  preview and thumbnail images of each page of uploaded PDF files and store
  them annotated onto the content object containing the PDF file.

* Image generation from the PDF file is processed asynchronously so that the
  user does not have to wait for the images to be created in order to continue
  using the site, as the processing of large PDF files can take many minutes to
  complete.

  Since ``2.0.0`` pdfpeek supports *rabbitmq* message queuing to generate
  thumbnails, see Installation_ section for more details

* When a file object is initialized or edited, PdfPeek checks to see if a PDF
  file was uploaded. If so, a ghostscript image conversion job is added to the
  pdfpeek job queue (or rabbitmq in case of ``collective.zamqp`` usage).

* If the file uploaded is not of content type 'application/pdf', an image
  removal job is added to the pdfpeek job queue. This job queue is processed
  periodically by a cron job or a zope clock server process. The image
  conversion jobs add the IPDF interface to the content object and store the
  resulting image preview and thumbnail for each page of the PDF annotated on
  to the content object itself. The image removal jobs remove the image
  annotations and the IPDF interface from the content object.

* If a job fails, it is removed from the processing queue and appended to a
  list of failed jobs. If a job succeeds, it is removed from the processing
  queue and appended to a list of successfully completed jobs.


Viewlet
-------

PdfPeek ships with an example user interface that is turned on by default. This
UI displays the thumbnail images of each page of the PDF file when a user views
the content object in their browser. This example UI is not quite working yet,
and is meant to be just that, an example. I don't claim to be a javascript
master.

A custom traverser is available to make it easy to access the images and
previews directly, as well as to build custom views incorporating image
previews of file content.

Installation
------------

Use ``zc.buildout`` to install. If you want asynchronous queue processing using
``collective.zamqp`` you may want to add ``collective.pdfpeek [zamqp]``. Use

- ``collective.pdfpeek [dexterity]`` for dexterity support
- ``collective.pdfpeek [archetype]`` for archetype support
- ``collective.pdfpeek [zamqp]`` for ``collective.zamqp`` support

You can also combine those extras as shown below (see ``buildout-zamqp.cfg``
for a working buildout configuration)::

    [buildout]
    ...
    parts =
        instance

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    eggs =
        ...
        collective.pdfpeek [dexterity, zamqp]

    zope-conf-additional =
        %import collective.zamqp
        <amqp-broker-connection>
            connection_id   superuser
            hostname        127.0.0.1
            port            5672
            username        guest
            password        guest
            heartbeat       120
            keepalive       60
        </amqp-broker-connection>

Configuration
-------------

PdfPeek ships with a configlet that allows the site administrator to adjust the
size of the generated preview and thumbnail images, as well as toggle the
example user interface and default event handlers on and off.


Requirements
------------

* Plone 4.1+

* Requires the GNU ghostscript gs binary to be available on the $PATH!

* Tested on POSIX compliant systems such as LINUX and MacOS 10.8.

* Untested on Windows systems. (Wouldn't be surprised if it works, as long as
  you can install gs.)*

* As of version 0.17, Plone 3.x is no longer officially supported.


Code, Issues, Comments
----------------------

* Code repository: https://github.com/collective/collective.pdfpeek

* Report bugs on github: https://github.com/collective/collective.pdfpeek/issues

* Questions and comments to db@davidbrenneman.com
