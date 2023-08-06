**Waliki** is an extensible wiki app for Django with a Git backend.


.. attention:: It's usable but in an early development stage. I'll appreciate your feedback and help.


.. image:: https://badge.fury.io/py/waliki.png
    :target: https://badge.fury.io/py/waliki

.. image:: https://travis-ci.org/mgaitan/waliki.png?branch=master
    :target: https://travis-ci.org/mgaitan/waliki

.. image:: https://coveralls.io/repos/mgaitan/waliki/badge.png?branch=master
    :target: https://coveralls.io/r/mgaitan/waliki?branch=master

.. image:: https://readthedocs.org/projects/waliki/badge/?version=latest
   :target: https://readthedocs.org/projects/waliki/?badge=latest
   :alt: Documentation Status

.. image:: https://pypip.in/wheel/waliki/badge.svg
    :target: https://pypi.python.org/pypi/waliki/
    :alt: Wheel Status

:home: https://github.com/mgaitan/waliki/
:demo: http://waliki.pythonanywhere.com
:documentation: http://waliki.rtfd.org
:group: https://groups.google.com/forum/#!forum/waliki-devs
:license: `BSD <https://github.com/mgaitan/waliki/blob/master/LICENSE>`_


At a glance, Waliki has this features:

- File based content storage.
- Version control and concurrent edition for your content using Git
- Extensible architecture with plugins
- Markdown or reStructuredText. Easy to add more.
- A simple ACL system
- Attachments
- UI based on Twitter's Bootstrap and Codemirror.
- Works with Python 2.7, 3.3+ or PyPy in Django 1.5 or newer

How to start
------------

Install it with pip::

    $ pip install waliki

Or the development version::

    $ pip install https://github.com/mgaitan/waliki/tarball/master


Add ``waliki`` and the optionals plugins to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'waliki',
        'waliki.git',           # optional but recommended
        'waliki.attachments',   # optional but recommended
        'waliki.pdf',           # optional
        'waliki.slides',        # optional
        ...
    )

Include ``waliki.urls`` in your project's ``urls.py``. For example::

    urlpatterns = patterns('',
        ...
        url(r'^wiki/', include('waliki.urls')),
        ...
    )

Sync your db::

    $ python manage.py syncdb


Enjoy!


Why "Waliki" ?
----------------

**Waliki** is an `Aymara <http://en.wikipedia.org/wiki/Aymara_language>`_ word that means *all right*, *fine*.

It sounds a bit like *wiki*, has a meaningful sense for this project
and also plays with the idea of using a non-mainstream language [1]_ .

And last but most important, it's a humble tribute to the bolivian president `Evo Morales <http://en.wikipedia.org/wiki/Evo_Morales>`_.

.. [1] *wiki* itself is a hawaiian word




Changelog
---------

0.3 (2014-11-11)
++++++++++++++++

- Plugin *attachments*
- Implemented *per namespace* ACL rules
- Added the ``waliki_box`` templatetag: use waliki content in any app
- Added ``entry_point`` to extend templates from plugins
- Added a webhook to pull and sync change from a remote repository (Git)


0.2 (2014-09-29)
++++++++++++++++

- Support concurrent edition
- Added a simple ACL system
- ``i18n`` support (and locales for ``es``)
- Editor based in Codemirror
- Migrated templates to Bootstrap 3
- Added the management command ``waliki_sync``
- Added a basic test suite and setup Travis CI.
- Added "What changed" page (from Git)
- Plugins can register links in the nabvar (``{% navbar_links %}``)

0.1.2 / 0.1.3 (2014-10-02)
++++++++++++++++++++++++++

* "Get as PDF" plugin
* rst2html5 fixes

0.1.1 (2014-10-02)
++++++++++++++++++

* Many Python 2/3 compatibility fixes

0.1.0 (2014-10-01)
++++++++++++++++++

* First release on PyPI.

