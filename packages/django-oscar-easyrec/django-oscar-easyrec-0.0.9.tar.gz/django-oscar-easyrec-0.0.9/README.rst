================================
Easyrec package for django-oscar
================================

This package provides integration with the recommendation system, `easyrec`_.  It is designed to
integrate seamlessly with the e-commerce framework `django-oscar`_.

.. _`easyrec`: http://easyrec.org/
.. _`django-oscar`: https://github.com/tangentlabs/django-oscar

Continuous integration status:

.. image:: https://travis-ci.org/snowball-one/django-oscar-easyrec.svg?branch=master
    :target: https://travis-ci.org/snowball-one/django-oscar-easyrec

.. image:: https://coveralls.io/repos/snowball-one/django-oscar-easyrec/badge.png?branch=master
    :target: https://coveralls.io/r/snowball-one/django-oscar-easyrec

Getting started
===============

Installation
------------

From PyPI::

    pip install django-oscar-easyrec

or from Github::

    pip install git+git://github.com/snowball-one/django-oscar-easyrec.git#egg=django-oscar-easyrec

Add ``'easyrec'`` to ``INSTALLED_APPS``.

You will also need to install

Instructions for installing Easyrec can be found on `easyrec's sourceforge wiki`_

.. _`easyrec's sourceforge wiki`: http://easyrec.sourceforge.net/wiki/index.php?title=Installation_Guide


Full documentation is available at `Read the Docs`_

.. _`Read the Docs`: https://django-oscar-easyrec.readthedocs.org/en/latest/
