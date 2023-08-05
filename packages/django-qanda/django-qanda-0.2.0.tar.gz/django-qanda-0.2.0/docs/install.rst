.. _install:

Installation
============

This part of the documentation covers the installation of Qanda.


Requirements
------------

Qanda currently runs on Django 1.4.2 or greater, Python 2.7 or greater.


Distribute & Pip
----------------

Installing Qanda is simple with `pip <https//:pip.pypa.io>`_, just run this in your terminal::

    $ pip install django-qanda

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install django-qanda

Using `pip is the recommended method <https://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install>`_.


Get the code
------------

Qanda is actively developed on Bitbucket, where the code is
`always available <https://bitbucket.org/mhurt/django-qanda>`_.

You can either clone the repository::

    $ hg clone https://bitbucket.org/mhurt/django-qanda

or download the `tar-ball or zip-ball of your choice <https://bitbucket.org/mhurt/django-qanda/downloads>`_.

Once you have a copy of the source, you can install it into
your site packages easily::

    $ python setup.py install


Configuring your project
------------------------

In your Django project's settings, add Qanda to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = {
      ...
      'qanda'
    }

Include the qanda URLconf in your project urls.py like this::

    url(r'^faq/', include('qanda.urls'))

In Django 1.7 run ``python manage.py migrate qanda``.
Otherwise, just run ``python manage.py syncdb``.


Sitemap
~~~~~~~

Qanda has a default sitemap ``qanda.sitemaps.QuestionSitemap`` which you can
use if providing sitemaps.xml for your project.
See 
`Django's sitemaps documentation <https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/>`_
for how to wire this up.
