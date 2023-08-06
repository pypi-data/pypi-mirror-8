****************
django-uecookie9
****************

Small app that detects if the current user is located in the European Union. If so, a small notification about cookies is displayed. Once notification is closed by the user, it will not appear anymore.

``uecookie9`` also creates a FlatPage with a Cookie Policy.

Requirements
============

- `pygeoip <https://pypi.python.org/pypi/pygeoip/>`_

- `django.contrib.flatpages <https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/>`_

Instalation
===========

- Install via pip::

    pip install django-uecookie9

- Add ``uecookie9`` to your ``INSTALLED_APPS``

- Add ``django.core.context_processors.request`` to your ``TEMPLATE_CONTEXT_PROCESSORS``::

	from django.conf import settings
	 TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + (
		'django.core.context_processors.request',
	)
    
- Override template ``uecookie9/policy.html`` with your actual Cookie Policy.

- Execute the command below (creates a FlatPage ``/cookies/``)::

	python manage.py uecookie9

Usage
=====

Paste the following code in the right place in your template::

	{% load uecookie9 %}{% uecookie9 %}


Customization
=============

By default, notification is wrapped in a fixed div that shows at the bottom of the page. In order to customize it you have to create your own version of template ``uecookie9/message.html``. 

Disclaimer
==========
There is no guarantee that this app is enough to meet UE requirements. Use at your own risk.

Notes
=====

- ``uecookie9`` was tested with Django 1.6.5, however it should work with newer or older versions as well.
- This application includes GeoLite2 data created by `MaxMind <http://www.maxmind.com>`_.

