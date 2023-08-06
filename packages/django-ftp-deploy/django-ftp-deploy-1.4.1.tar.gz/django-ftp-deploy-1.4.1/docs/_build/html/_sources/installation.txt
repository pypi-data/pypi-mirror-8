.. _installation:

Installation
============

Installation and requirements for django-ftp-deploy module


Requirements
------------

#.  Django 1.5, 1.6
#. `celery <http://www.celeryproject.org/>`_
#. `pycurl <https://pypi.python.org/pypi/pycurl>`_
#. `certifi <https://pypi.python.org/pypi/certifi>`_
#. `django_braces <https://pypi.python.org/pypi/django-braces>`_
#. `django_crispy_forms <https://pypi.python.org/pypi/django-crispy-forms>`_

Required third party libraries are **installed automatically** if you use pip to install django-ftp-deploy.



Installation
------------

.. note:: FTP Deploy Server is optional and doesn't need to be installed for basic usage. It is however, highly recommended that you install FTP Deploy Server to gain full functionality.


#. The recommended way to install the Django FTP Deploy is via pip::

        pip install django-ftp-deploy

   If you aren't familiar with pip, `download <https://pypi.python.org/pypi/django-ftp-deploy/>`_  a copy of the ``ftp_deploy`` and add it to your Python path. You need to install all `requirements`_ manually as well.

#. Add ``ftp_deploy`` and ``ftp_deploy.server`` to your ``INSTALLED_APPS`` setting:

   .. code-block:: python

    #settings.py

    INSTALLED_APPS = (
      ...
      'ftp_deploy',
      'ftp_deploy.server',
      ...
    )

#. Make sure you have ``django.core.context_processors.request`` in your ``TEMPLATE_CONTEXT_PROCESSORS`` setting:

   .. code-block:: python

    #settings.py

    TEMPLATE_CONTEXT_PROCESSORS = (
      ...
      'django.core.context_processors.request',
      ...
    )

#. Add the ``ftp_deploy`` URLs to your project URLconf as follows:

   .. code-block:: python

        #projectname/urls.py

        urlpatterns = patterns('',
            ...
            url(r'^ftpdeploy/', include('ftp_deploy.urls')),
            url(r'^ftpdeploy/', include('ftp_deploy.server.urls')),
            ...
          )

#. Synchronize your database. It is highly recommended you use `south <https://pypi.python.org/pypi/South/>`_ migration tool

   .. code-block:: python

        python manage.py migrate ftp_deploy



#. Copy static files into your ``STATIC_ROOT`` folder

   .. code-block:: python

       python manage.py collectstatic


Configuration
-------------
* Add folder containing ``settings.py`` file to your Python path

* Add ``DEPLOY_BITBUCKET_SETTINGS`` and/or ``DEPLOY_GITHUB_SETTINGS`` configuration to your settings::

    #settings.py

    DEPLOY_BITBUCKET_SETTINGS = {
      'username'      : '',
      'password'      : '',
    }

    DEPLOY_GITHUB_SETTINGS = {
      'username'      : '',
      'password'      : '',
    }

* Set `django_crispy_forms <https://pypi.python.org/pypi/django-crispy-forms>`_ template pack to *bootstrap 3*

  .. code-block:: python

      #settings.py
      CRISPY_TEMPLATE_PACK = 'bootstrap3'

* Add celery configuration::

    #settings.py
    BROKER_URL = ''
    CELERY_RESULT_BACKEND=''
    #settings depends on message broker and result backend, see example below

* Go to your project root folder and run celery worker as follow::

    celery -A ftp_deploy worker --concurrency 1

  .. note:: Celery example above apply only for development enviroment. Celery worker in production should be run as a deamon. Read more in Celery `documentation <http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html>`_.

  .. warning:: Remember to include '*--concurrency 1*' option when running the worker. That avoid to perform more then one task at the same time.

Celery - RabbitMQ
*****************

If you are using Ubuntu or Debian install RabbitMQ by executing this command::

    sudo apt-get install rabbitmq-server

* Update celery configuration as follows::

    #settings.py
    BROKER_URL = 'amqp://'
    CELERY_RESULT_BACKEND='amqp'


Celery - django
***************

.. note:: Configuration presented below use django as a broker and result backend, however this is not recommended for production enviroment. Read more in Celery `documentation <https://celery.readthedocs.org/en/latest/>`_.

In order to use django as broker and backend, project need to have  `django-celery <https://pypi.python.org/pypi/django-celery>`_ project installed:

* Install django-celery using pip::

    pip install django-celery

* Add *djcelery* to your ``INSTALLED_APPS`` setting

  .. code-block:: python

   #settings.py

   INSTALLED_APPS = (
     ...
     'kombu.transport.django',
     'djcelery',
     ...
   )

* Update celery configuration as follows::

    #settings.py
    BROKER_URL = 'django://'
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

* Synchronize your database using `south <https://pypi.python.org/pypi/South/>`_::

    python manage.py migrate djcelery
    python manage.py migrate kombu.transport.django
