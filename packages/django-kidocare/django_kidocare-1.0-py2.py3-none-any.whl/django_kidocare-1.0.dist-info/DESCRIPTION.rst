#########
Kido Care
#########

Goal
====

Provide tool which help finding performance issues in django projects.

Installation
============

Install Kido Care:

.. code-block:: console

   pip install django-kidocare

or current development version:

.. code-block:: console

   pip install hg+https:://bitbucket.org/kidosoft/django-kidocare

Configuration
=============

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'kidocare',
        ...
    )

Usage
=====

Checking for queries run at startup::

    $ python manage.py check_startup_queries -o queries.txt

Supported Django versions
=========================

Tested with: 

* Django 1.2.7 on python2.7
* Django 1.3.7 on python2.7
* Django 1.4.16 on python2.7
* Django 1.5.11 on python2.7, python3.4
* Django 1.6.8 on python2.7, python3.4
* Django 1.7.1 on python2.7, python3.4


