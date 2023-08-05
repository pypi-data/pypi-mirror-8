.. _exampleproject:


Example Project
===============

First you'll need to ensure that you've :doc:`installed</install>`
Qanda, and that you also have a recent install of Django itself.

Next, in your terminal you'll want to run through the Django project setup.
Assuming you're already in the ``django-qanda`` directory::

        $ cd example/
        $ python manage.py syncdb

This will create the SQLite database *in the current directory*. Follow the
on-screen prompts as with any Django project.

Skip this part if you want to get started straight away or, if you'd like to
load the sample data for Qanda you can run the following command to
import the supplied fixtures::

        $ python manage.py loaddata ../qanda/fixtures/qanda_example.json

At this point you're ready to play with the example project, and you can simply
run Django's development server as normal::

        $ django manage.py runserver

Finally, log into the admin area at ``http://127.0.0.1:8000/admin/``, or go to
``http://127.0.0.1:8000/faq/`` to take a look at the templates in action.


