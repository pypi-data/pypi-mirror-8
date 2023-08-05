Django MSSQL Database Backend
=============================

`Django-sqlserver`_ provies a Django database backend for Microsoft SQL Server.
It supports: ADO via PyWin32, python-tds (native python TDS driver) and pymssql (FreeTDS python binding)

Requirements
------------

    * Python 2.7, 3.3

SQL Server Versions
-------------------

Supported Versions:
    * 2005
    * 2008
    * 2008r2
    * 2012

The SQL Server version will be detected upon initial connection.

Django Version
--------------

The current version of django-sqlserver supports Django 1.6. If using an older
version of Django, you will need to use an earlier version of django-sqlserver.

django-sqlserver 0.5 supports Django 1.4 and 1.5.

References
----------

    * Django-sqlserver on PyPi: http://pypi.python.org/pypi/django-sqlserver
    * DB-API 2.0 specification: http://www.python.org/dev/peps/pep-0249/


.. _`Django-sqlserver`: https://bitbucket.org/cramm/django-sqlserver
