.. _getinvolved:

Introduction
============

#. Clone ``django-ftp-deploy`` app::

    git clone https://bitbucket.org/lpakula/django-ftp-deploy.git

#. Add ``django-ftp-deploy`` folder to your Python path

#. Install application as described in :ref:`installation <installation>` section.

#. Install all requirements for dev environment. Go to ``django-ftp-deploy`` directory and use pip::

     pip install -r requirements/dev.txt

#. Add ``FTP_TEST_SETTINGS`` configuration to your

   .. code-block:: python

       #settings.py

       FTP_TEST_SETTINGS =  {
        'host'      : '',
        'username'  : '',
        'password'  : '',
        'path'      : '',
       }

#. Make sure ``DEPLOY_BITBUCKET_SETTINGS`` and ``DEPLOY_GITHUB_SETTINGS`` both have been added to settings file.

#. Install `PhantomJS <http://phantomjs.org/>`_ for intergration tests.

#. **Start Developing!**


Testing
=======

Application use `Nose <https://nose.readthedocs.org/en/latest/>`_ as test runner and  `Fabric <http://docs.fabfile.org/en/1.8/>`_ library to automate testing process.

In order to run tests go into *tests* directory and:


* *all* tests::

   fab test

* *all* tests with *coverage*::

   fab testc

* *Unit Tests* only::

   fab testu

* *Integration Tests* only::

   fab testi


*Unit Tests* and *Integration Tests* accepts **module** attibute to specify module to test::

   fab testu:module_name
