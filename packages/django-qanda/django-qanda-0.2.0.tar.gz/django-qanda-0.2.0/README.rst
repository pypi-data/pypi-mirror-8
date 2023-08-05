Django-Qanda
============

Qanda is a simple FAQ app for the Django framework.

Questions can be displayed publicly, to logged-in users, or to site staff only.

Questions are organised by topic, and those topics are self-hiding depending on
the publication status of the questions inside.

Qanda installs with fully styled templates so that you can start playing
straight away, and an example project is supplied.


.. image:: http://django-qanda.readthedocs.org/en/latest/_images/qanda-threepage.png
   :alt: Screenshots of qanda default templates

For more information please see the documentation at http://django-qanda.readthedocs.org/en/latest/.

.. image:: https://readthedocs.org/projects/django-qanda/badge/?version=latest
   :target: http://django-qanda.readthedocs.org/en/latest/
   :alt: Documentation Status


Requirements
------------

- Django 1.4.2 or greater;
- Python 2.7 or greater.


Get It
------

You can `get Qanda <https://pypi.python.org/pypi/django-qanda/>`_  by using pip or easy_install::

    $ pip install django-qanda
    or
    $ easy_install django-qanda

If you want to install it from source, grab the Mercurial repository from Bitbucket::

    $ hg clone https://bitbucket.org/mhurt/django-qanda
    $ cd django-qanda
    $ python setup.py install


Install It
----------

Add "qanda" to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = {
      ...
      'qanda'
    }

Include the qanda URLconf in your project urls.py like this::

    url(r'^faq/', include('qanda.urls'))


For Django 1.7 users, run ``python manage.py migrate`` to create the qanda
models. Otherwise simply run ``python manage.py syncdb``.


Contribute
----------

- Issue Tracker: https://bitbucket.org/mhurt/django-qanda/issues
- Source Code: https://bitbucket.org/mhurt/django-qanda/
- Documentation:  http://django-qanda.readthedocs.org/en/latest/


License
-------

The project is licensed under the MIT license.
