.. Django FTP Deploy documentation master file, created by
   sphinx-quickstart on Mon Oct  7 18:49:46 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django FTP Deploy Documentation
============================================

django-ftp-deploy allows you to automatically deploy GIT repositories to FTP servers. You don't need to install git on the server!


**Features:**

* Manage multiple services (a service is one repository-to-ftp configuration)
* Verification service configuration
* Repository hook management
* Restore failed deploys
* Email notifications
* Logs and Statistics


Supported GIT repositories:

* Bitbucket
* Github


Current tests coverage status:

.. image:: ../tests/coverage/coverage_status.png


User Guide
----------


.. toctree::
   :maxdepth: 3

   installation
   usage
   other
   changelog


Get Involved!
-------------

Get involved and help make this app better!

.. toctree::
   :maxdepth: 3

   getinvolved



Roadmap
-------

* Cron validation
* FTP password encryption
* Advanced statistics
* Support multi queues




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

