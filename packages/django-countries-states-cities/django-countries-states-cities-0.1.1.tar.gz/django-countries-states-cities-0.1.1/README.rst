.. role:: python(code)
   :language: python

########################################
django-countries-states-cities
########################################

*****
Usage
*****

0. Installation
===============

The preferred installation method is directly from pypi:

.. code:: console

   pip install -U django-countries-states-cities

.. _readme-quickstart:

1. Quickstart
=============

1. In ``settings.py``:

.. code:: python

    INSTALLED_APPS = [
        'modeltranslation',
        'django.contrib.admin',
        ...
        'countries_states_cities'
    ]

    def gettext_noop(s):
        return s

    LANGUAGES = [  # supported languages
        ("en", gettext_noop("English")),
        ("ja", gettext_noop("Japanese")),
        ("ko", gettext_noop("Korean")),
    ]

2. In ``urls.py``:

.. code:: python

    urlpatterns = [
        ...
        path('csc/', include('countries_states_cities.urls')),
    ]

3. Run ``python manage.py migrate`` to create the countries_states_cities models.

2. Configuration
================

Todo...