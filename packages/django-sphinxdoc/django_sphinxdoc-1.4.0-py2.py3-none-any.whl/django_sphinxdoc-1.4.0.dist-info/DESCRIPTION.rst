===============================================================
django-sphinxdoc – Embed your Sphinx docs into your Django site
===============================================================

This Django application allows you to integrate any `Sphinx
<http://sphinx.pocoo.org/>`_ documentation directly into your Django powered
website instead of just serving the static files.

Django-sphinxdoc can handle multiple Sphinx projects and offers a `Haystack
<http://haystacksearch.org/>`_ powered search. Future versions will enable
comments and add RSS feeds.


Requirements
------------

This app requires Django >= 1.4.2, Sphinx >= 1.0 and Haystack >= 2.1.


Installation
------------

Just use `PIP <http://pypi.python.org/pypi/pip>`_:

.. sourcecode:: bash

    $ pip install django-sphinxdoc

If you want the lates development version, isntall it from Bitbucket:

.. sourcecode:: bash

    $ pip install https://ssc@bitbucket.org/ssc/django-sphinxdoc
    $ # or
    $ hg clone ssh://hg@bitbucket.org/ssc/django-sphinxdoc
    $ pip install -e django-sphinxdoc


Usage
-----

The Documentation can be found in the *docs/* directory.



Changelog for django-sphinxdoc
==============================

v1.4 – 2014-12-14:
------------------

- [NEW] Support for Python 3 (3.3 and above)


v1.3 – 2014-03-05:
------------------

- [NEW] Projects can now be protected authentication.


v1.2.1 – 2013-12-20:
--------------------

- [NEW] Option ``--all`` to update docs for all projects
- [NEW] Filters for the project admin
- [NEW] Setting: ``SPHINXDOC_CACHE_MINUTES``
- [NEW] Setting: ``SPHINXDOC_BUILD_DIR``
- [FIX] Titles for generated domain indexes


v1.2 – 2013-08-11:
------------------

- [NEW] I18n and l10n for Spanish and Basque, by Ales Zabala Alava
- [CHANGE] Use class-based views, by Josiah Klassen
- [CHANGE] Migration to Haystack 2, by Andres Riancho
- [FIX] Inclusion of search index template in package, by Mike Shantz


v1.1 – 2012-04-19:
------------------

- [NEW] Support static and download files.
- [NEW] Additional context to search view so that project information is
  available in the template.
- [CHANGE] Updated some `templates
  <https://bitbucket.org/ssc/django-sphinxdoc/changeset/e876d5e72b34>`_
- [FIX] Fixed a bug with the updatedoc command and ``~`` in paths.
- [FIX] Include all module index files.
- [FIX] Improved indexing behaviour
- [FIX] Improved behaviour when building the docs.


v1.0.0 – 2010-09-11:
--------------------

- [NEW] Documentation can be searched via Haystack. The new management command
  ``updatedoc`` imports the JSON files into the database and updates Haystack’s
  search index.
- [CHANGE] Renamed ``App`` to ``Project``.


v0.3.2 – 2010-03-14:
--------------------

- [FIX] Fixed a bug in ``setup.py``.


v0.3.1 – 2010-03-11:
--------------------

- [CHANGE] Repackaging


v0.3 – 2010-01-06:
------------------

- [NEW] Views for images, sources and object inventory


v0.2 – 2009-12-30:
------------------

- [NEW] Documentation, general index and module index work
- [NEW] Basic documentation written


v0.1 – 2009-12-19:
------------------

- [NEW] Initial release



Authors
=======

The primary author of django-sphinxdoc is Stefan Scherfke, who may be found
online at http://stefan.sofa-rockers.org/.

Contributors:

- `Mitar <https://bitbucket.org/mitar>`_
- `Mike Shantz <https://bitbucket.org/mikeshantz>`_
- `Josiah Klassen <https://bitbucket.org/jkla>`_
- `Andres Riancho <https://bitbucket.org/andresriancho>`_
- `Ales Zabala Alava <https://bitbucket.org/shagi>`_
- `Ianaré Sévi <https://bitbucket.org/ianare>`_
- Romain Beylerian
- Bosco Mutunga


