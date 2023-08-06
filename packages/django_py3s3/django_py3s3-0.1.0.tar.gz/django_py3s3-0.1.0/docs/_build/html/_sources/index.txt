.. django_py3s3 documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django_py3s3 | Django + AWS S3 + Python 3.3+
============================================

A Django storage backend for saving files to AWS S3.

.. toctree::
   :maxdepth: 2

Installation
------------

::

    pip install django_py3s3

Then add to your settings.py file::

    INSTALLED_APPS = (
        ...
        'django_py3s3',
        ...
    )
    
    STATICFILES_STORAGE = 'django_py3s3.storages.S3StaticStorage'
    DEFAULT_FILE_STORAGE = django_py3s3.storages.S3MediaStorage'


    # AWS file access info
    AWS_ACCESS_KEY_ID = '<your access key>'
    AWS_SECRET_ACCESS_KEY = '<your secret key>'
    AWS_STORAGE_BUCKET_NAME = '<your bucket name>'



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
