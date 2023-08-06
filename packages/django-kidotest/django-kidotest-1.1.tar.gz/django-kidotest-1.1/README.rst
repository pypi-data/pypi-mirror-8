##########
Kido Test
##########

Goal
====

Provide code snippets which help running tests in Django.

Installation
============

Install requirements:

.. code-block:: console
    
    pip install mock

Install Kido Test:

.. code-block:: console

   pip install django-kidotest

or current development version:

.. code-block:: console

   pip install hg+https:://bitbucket.org/kidosoft/django-kidotest

Configuration
=============

.. code-block:: python

   INSTALLED_APPS =  [
    ...
    'kidotest',
    ...
   ]

Usage
=====

Supported Django versions
=========================

Tested with: 

* Django 1.2.7 on python2.7
* Django 1.3.7 on python2.7
* Django 1.4.16 on python2.7
* Django 1.5.11 on python2.7, python3.4
* Django 1.6.8 on python2.7, python3.4
* Django 1.7.1 on python2.7, python3.4
