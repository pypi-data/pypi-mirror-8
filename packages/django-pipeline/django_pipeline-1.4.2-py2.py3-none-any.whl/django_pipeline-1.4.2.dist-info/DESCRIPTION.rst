Pipeline
========

Pipeline is an asset packaging library for Django, providing both CSS and
JavaScript concatenation and compression, built-in JavaScript template support,
and optional data-URI image and font embedding.

Installation
------------

To install it, simply: ::

    pip install django-pipeline


Documentation
-------------

For documentation, usage, and examples, see :
http://django-pipeline.readthedocs.org


.. :changelog:

History
=======

1.4.2
=====

* Fix finder bug. Thanks to Quentin Pradet, Remi and Sam Kuehn for the report
* Update finders documentation. Thanks to Thomas Schreiber, Grégoire Astruc and Tobias Birmili for the report.

1.4.1
=====

* Fix storage logic. Thanks to Quentin Pradet for the report.

1.4.0
=====

* **BACKWARD INCOMPATIBLE** : Renamed templatetags library from ``compressed`` to ``pipeline``.
* **BACKWARD INCOMPATIBLE** : Renamed templatetag ``compressed_js`` to ``javascript``.
* **BACKWARD INCOMPATIBLE** : Renamed templatetag ``compressed_css`` to ``stylesheet``.


