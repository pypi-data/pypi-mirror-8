django_py3s3
============


Installation
------------

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


Contributing
------------

To contribute to django_py3s3 `create a fork`_ on GitHub. 
Clone your fork, make some changes, and submit a pull request.

.. _create a fork: https://github.com/logston/django_py3s3

Issues
------

Use the GitHub `issue tracker`_ for django_py3s3 to submit bugs, issues, and feature requests.

.. _issue tracker: https://github.com/logston/django_py3s3/issues

