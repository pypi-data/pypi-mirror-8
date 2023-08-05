=====
Qanda
=====

Qanda is a simple FAQ app for the Django framework


Get It
------

You can get Qanda by using pip or easy_install::

    $ pip install django-qanda
    or
    $ easy_install django-qanda

If you want to install it from source, grab the Mercurial repository from Bitbucket::

    $ hg clone https://mhurt@bitbucket.org/mhurt/django-qanda
    $ cd django-qanda
    $ python setup.py install


Install It
----------

1. Add "qanda" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = {
      ...
      'qanda'
    }

2. Include the qanda URLconf in your project urls.py like this::

    url(r'^faq/', include('qanda.urls'))


3. Run :code:`python manage.py migrate` to create the qanda models.

4. Start the development server and visit http://127.0.0.1:8000/admin/ to
   start creating new questions (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/faq/ to view your questions.


Contribute
----------

- Issue Tracker: https://bitbucket.org/mhurt/django-qanda/issues
- Source Code: https://bitbucket.org/mhurt/django-qanda/


License
-------

The project is licensed under the MIT license.