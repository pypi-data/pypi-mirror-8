================== 
cmsplugin-feedback
================== 
.. image:: https://travis-ci.org/satyrius/cmsplugin-feedback.svg?branch=master

Feedback form plugin for Django CMS [#]_

.. image:: https://cloud.githubusercontent.com/assets/278630/5002184/c4bbe36a-6a0e-11e4-8c5d-024ec11d2c94.png

Requirements
============

Python
------
It works fine and tested under ``Python 2.7``. The following libraries are required

- ``Django`` 1.5 or 1.6 (we droped support for Django 1.4, and do not support Django 1.7)
- ``django-cms`` >= 3.0 (we recommend you to use Django CMS 3.0 and higher, contact us if you need prior CMS versions supports and have some issues)
- ``django-simple-captcha`` >= 0.4.1

JavaScipt
---------

The feedback form use ``jQuery`` to post form data asynchronously.
You should take care of this library and include it to your page directly, 
or to add it to your assets builder, etc.

Installation
============
This library is under development and is not published on *pipi*, so you have to install it from repository by branch name, tag or commit hash ::

  $ pip install -e git@github.com:satyrius/cmsplugin-feedback.git@master#egg=cmsplugin_feedback
  
Update your ``settings.py`` ::

  INSTALLED_APPS = [
      # django contrib and django cms apps
      'captcha',
      'cmsplugin_feedback',
  ]
  
Do not forget to include urls to ``urls.py`` ::

  urlpatterns = patterns('',
      url(r'^captcha/', include('captcha.urls')),
      url(r'^feedback/', include('cmsplugin_feedback.urls')),
      url(r'^', include('cms.urls')),
  )

And to migrate your database ::

  django-admin.py migrate captcha cmsplugin_feedback
  
Roadmap
=======
- Translations
- Django 1.7 and Python 3 support
- Both sync and async form posting workflow. To cover number of cases — no javascript (realy?); no jquery on the page; you dont want to use async workflow and want to refresh a page.
- Form without captcha (if you dont need it or for registered users)

Contributing
============
Fork the repo, create a feature branch then send me pull request. Feel free to create new issues or contact me using email.

.. [#] Form style depends on your design, this is just an example. You should customize it with your own CSS.
