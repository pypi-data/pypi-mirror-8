.. django-qanda documentation master file, created by
   sphinx-quickstart on Sun Sep 28 18:15:05 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-qanda's documentation!
========================================

Qanda is a simple FAQ app for `Django <https://www.djangoproject.com/>`_ projects.

Here are the main features:

- Published questions can be made public, restricted to logged-in users, or only
  visible to site staff.

- Topics are self-hiding depending on the access level of the questions they
  contain.

- Qanda installs with a fully working set of templates so you can start playing
  straight away.

You can get started with :doc:`user/install`

Screenshots
-----------

Because everyone loves screenshots, here are the three default views that Qanda
installs with...



.. figure:: /images/qanda-topiclist-shadow.png

   Topic List

   The topic list is 'index' page of the app. It shows both the available topics
   and a list of the most recently modified questions.



.. figure:: /images/qanda-topicdetail-shadow.png

   Topic Detail

   Clicking into a particular topic, this page shows the available questions in
   that topic with brief information such as the modification date and an
   extract of the published answer.



.. figure:: /images/qanda-questiondetail-shadow.png

   Question Detail

   Diving into a chosen question you can read the answer in full. This view
   also provides quick links to other questions in the same topic.

Contents:

.. toctree::
   :maxdepth: 2

   user/install


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

