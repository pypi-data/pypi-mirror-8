Changelog
=========

2.0.0 (2014-12-04)
------------------

- Update ``README.rst`` to include a configuration example
  [saily]

- Fix failing tests by including metadata into annotation storage of
  processed files. Test updates.
  [saily]

- Use ``abc.ABCMeta`` as metaclass for abstract base class.
  [saily]

- Fix dependencies and don't include ``collective.zamqp`` into tests to allow
  test of default event handlers.
  [saily]

- Updated events and added subscriber for ``IObjectCreatedEvent``.
  [agitator]

- Drop support for Plone 4.1, Fix test setup with ``plone.app.contenttypes``.
  [saily]

- Flake8, PEP8 cleanup, remove double quotes, PEP3101, jshint, jscs and csslint
  checks using ``plone.recipe.codeanalysis``. This is also done on travis.
  [saily]

- Update ``buildout`` and travis config.
  [saily]

- Update ``bootstrap.py`` for buildout 2.x.
  [saily]


2.0b2 (2013-10-17)
------------------

- Fix missing README.rst in package.
  [saily]


2.0b1 (2013-10-17)
------------------

- Add a basic behavior to allow users to create PDF thumbnails for their own
  dexterity content types.
  [saily]

- Add ``collective.zamqp`` integration to allow queuing PDF thumbnail jobs into
  RabbitMQ message queuing server.
  [saily]

- Switch to PyPDF2 which is maintained compared to pyPdf and can be used as
  a drop-in replacement.
  [saily]

- Add travis-ci for Plone 4.1, Plone 4.2 and Plone 4.3.
  [saily]

- Use ``plone.app.testing`` and layers for tests. Add more tests for dexterity
  and ATContentTypes.
  [saily]

- Huge refactoring to replace transformers and functions with more flexible
  adapters.
  [saily]

- Plone 4.3 compatibility by removing deprecated imports from
  ``zope.app.component``.
  [saily]

- Add a new ``.gitignore`` file.
  [saily]

- Add egg-contained buildout. Rename ``*.txt`` to ``*.rst`` to support github
  markup directly.
  [saily]

- Dexterity types integration with field retrieval using IPrimaryFieldInfo
  adapter. This brings full functionality for ``plone.app.contenttypes``.
  [saily]

- Updated docs.
  [saily]


1.3 (2011-05-31)
----------------

 - Switched to PNG from JPEG.
   [dbrenneman]

1.2 (2010-12-7)
----------------

 - Fixed issue where local utilities would clash if pdfpeek was installed on
   multiple Plone instances within the same zope.
   [dbrenneman]

 - Fixed uninstall profile so that local persistent utilities are removed and
   image annotations are removed on uninstall of product.
   [dbrenneman]

1.0 (2010-5-27)
----------------

 - Fixed jQuery UI.
   [reedobrien]

0.19 (2010-4-8)
----------------

 - Modified transform to use cStringIO instead of StringIO, in the hopes of making things more efficient.
   [dbrenneman]

 - Modified conversion function to grab file data from object using getFile method, as this is the *proper* way of doing things...
   [dbrenneman]

0.18 (2010-2-26)
----------------

 - Fixed bug in reST rendering of changelog.
   [dbrenneman]

0.17 (2010-2-26)
-----------------

 - Added wide variety of pdf files to run through the unit tests for the
   ghostscript image transform.
   [dbrenneman]

 - Added unit tests for low level ghostscript transform.
   [dbrenneman]

 - Refactored transform code to make class and method names make more sense.
   [dbrenneman]

 - Updated README, including instructions for configuring the clock server.
   [dbrenneman]

 - Added asyncronous processing queue for ghostscript transform jobs.
   [dbrenneman]

 - Updated functional doctests to work on Plone 4 with blobfile storage.
   [dbrenneman]

 - Updated functional doctests to test transform queue.
   [dbrenneman]

 - Updated documentation.
   [dbrenneman]

 - Added unit testing harness.
   [dbrenneman]

0.16 (2009-12-12)
-----------------

 - Bugfix release.
   [dbrenneman]

0.15 (2009-12-12)
-----------------

 - Added configurable preview and thumbnail sizes.
   [claytron]

 - reST police! Fixing up the docs so that they might get rendered
   correctly.
   [claytron]

0.13 (2009-11-12)
-----------------

 - Refactored transform code to deal with encrypted pdf files better.
   [dbrenneman]

 - Made transform code more robust.
   [dbrenneman]

 - Added ability to toggle default event handler on and off.
   [dbrenneman]

0.12 (2009-10-25)
-----------------

 - Bugfix release.
   [dbrenneman]

0.11 (2009-10-25)
-----------------

 - Bugfix release.
   [dbrenneman]

0.10 (2009-10-25)
-----------------

 - Added code to check for EOF at the end of the pdf file data string and to
   insert one if it is not there. Fixes many corrupt pdf files.
   [dbrenneman]

0.9 (2009-10-13)
----------------

 - Fixed another bug in the transform code to allow functioning with any
   filefield, as long as it is called file.
   [dbrenneman]

0.8 (2009-10-13)
----------------

 - Fixed a bug in the transform code to allow functioning with any filefield,
   as long as it is called file.
   [dbrenneman]

0.7 (2009-10-13)
----------------

 - Streamlined transform code.
   [dbrenneman]

 - Added ability to toggle the pdfpeek viewlet display on and off via configlet.
   [dbrenneman]

0.6 (2009-10-05)
----------------

 - Bugfix release.
   [dbrenneman]

0.5 (2009-10-05)
----------------

 - Added control panel configlet.
   [dbrenneman]

 - Removed unneeded xml files from uninstall profile.
   [dbrenneman]

 - Optimized transform.
   [dbrenneman]

 - Added storage of image thumbnail along with image, generated with PIL.
   [dbrenneman]

 - Changed annotation to store images in a dict instead of a list.
   [dbrenneman]

 - Changed event handler to listen on all AT based objects instead of ATFile.
   [dbrenneman]

 - Added custom pdfpeek icon for configlet.
   [dbrenneman]

 - Added custom traverser to allow easy access to the OFS.Image.Image()
   objects stored on IPDF objects.
   [dbrenneman]

 - Modified pdfpeek viewlet code to display images using the custom traverser.
   [dbrenneman]

 - Added custom scrollable gallery with tooltips using jQuery Tools to the
   pdfpeek viewlet for display.
   [dbrenneman]

0.4 (2009-10-01)
----------------

 - Refactored storage to use OFS.Image.Image() objects instead of storing the
   raw binary data in string format.
   [dbrenneman]

 - Refactored event handler object variable name.
   [dbrenneman]

 - Removed unneeded files from default GS Ext. profile.
   [dbrenneman]

 - Removed unneeded javascript files and associated images and css.
   [dbrenneman]

0.3 - 2009-08-03
----------------

- fixed parsing of pdf files with multiple pages
  [piv]

0.1 - Unreleased
----------------

- Initial release
