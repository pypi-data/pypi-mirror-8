Changelog
=========

1.3.2 (2014-12-10)
------------------

- Ported a bugfix closed in the original TinyMCE file plugin.
  See `@0082163c6d`__ 
  [keul]

__ https://github.com/plone/Products.TinyMCE/commit/0082163c6d4ccdd5b4f55e330807297999030b8f

1.3.1 (2014-06-20)
------------------

- Fixed CSV icon (similar to `pull request #2`__ on collective.mtrsetup)
  and setted as non-binary
  [keul]
- Support for *odp* file
  [keul]
- Changed icon for *zip* and *rar*
  [keul]

__ https://github.com/collective/collective.mtrsetup/pull/2

1.3.0 (2014-05-27)
------------------

- Now depends on `collective.mtrsetup`__ to support also
  a lot of additional mime types [keul]
- New CSV support [giacomos, keul]
- Default icon for unknow file [giacomos, keul]

__ https://pypi.python.org/pypi/collective.mtrsetup

1.2.1 (2013-09-18)
------------------

- Fixed a JavaScript error when referencing non-file contents [keul]
- Do not display the additional file's information when not referencing file
  types [keul]

1.2.0 (2013-02-27)
------------------

- Restored the default TinyMCE link suffix as default [keul]
- Added a new adapter option: ``default_suffix``, to be able to
  control link type defaul by type [keul]
- ``IFileSuffixes`` adapters are now multiapdaters (using request also)
  so customizing types with browserlayer will be possible [keul]

1.1.0 (2012-12-05)
------------------

* Fixed plugin (removed ``region-content`` id) [keul]
* Added label for additional info in file popup [keul]
* i18n support (and italian translation provided) [keul]
* Now uninstall cleanly [keul]
* Added link format inside advanced settings [keul]
* Now supporting new advanced and pluggable option: "*Link format*"
  to handle how the URL to file is created [keul]
* Added support for internal link to image content type [keul]

1.0.0 (2012-10-10)
------------------

* Fixed Plone 4 compatibility icons drawing in popup template [cekk]

0.2.1 (2012-04-20)
------------------

* Version 0.2.0 was not upgrading properly [keul]

0.2.0 (2012-04-20)
------------------

* now require ``z3c.jbot`` because to fix a bug related to a broken context menu
  [keul]
* no more using a separate link plugin, but we are forced to use the original
  ones (for the fix above) [keul]
* added a product layer [keul]
* updated template and code to Product.TinyMCE 1.2 family [keul]

0.1.0 (2011-10-13)
------------------

* *University of Ferrara* provided some more CSS rules for better integration
  with MS Office files [keul]

0.0.1alpha (2010-07-20)
-----------------------

* initial release
