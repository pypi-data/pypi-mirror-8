Changelog
=========

0.2a1 - 2014-09-24
------------------

* Fixed problem with deprecation warning (django simplejson)

0.1c1 - 2012-08-25
------------------

* A few documentation fixes. Thanks Paolo Dina.

0.1b2 - 2012-05-08
------------------

* Fixed problem with initializing the editor in FeinCMS when adding new
  content blocks.

0.1b1 - 2012-05-08
------------------

* Textarea to editor conversion and live preview now also works for standard
  models, in collapsed fieldsets, added inlines and when switching tabs
  in FeinCMS pages.

0.1a2 - 2012-05-03
------------------

* Added jQuery plugin for CodeMirror initialization and preview updating.
  Thanks to Gustav Pursche!

* Improved usage and installation docs.

0.1a1 - 2012-04-27
------------------

* Initial release including ``MarkupMirrorField`` field,
  ``MarkupMirrorTextarea`` and ``AdminMarkupMirrorTextareaWidget`` widgets and
  providing FeinCMS integration with ``MarkupMirrorContent`` Page content-type.
  Supported markup types are plain text, HTML, Mardown, reStructuredText and
  Textile.
