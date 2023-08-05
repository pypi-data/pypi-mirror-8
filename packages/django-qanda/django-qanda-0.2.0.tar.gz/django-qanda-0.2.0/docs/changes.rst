.. _changes:

Changes
=======

To see all commits please visit https://bitbucket.org/mhurt/django-qanda/commits/all.


0.2.0
-----

(since v.0.1.0)

New:

- Added qanda.sitemaps.QuestionSitemap.
  Sitemap added to example app, and installation doc updated.

- Support Django 1.4.2 or higher.


Fixed:

- Incorrect homepage URL in setup script.
- Broken queryset access in TopicManager.for_staff()
- ... a lot of other bugs (sigh).

Changed

- Tox testenvs names now have shortened format, e.g ``py27dj17``.
- Documentation updates.
- Moved test runner to qanda.test.run
- Improved test suite


