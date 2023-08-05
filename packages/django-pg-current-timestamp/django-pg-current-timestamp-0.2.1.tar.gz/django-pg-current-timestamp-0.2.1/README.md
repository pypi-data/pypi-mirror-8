# Django Postgres Current Timestamp

.. image:: https://api.travis-ci.org/threatstream/django-pg-current-timestamp.png
   :alt: Build Status
   :target: https://travis-ci.org/threatstream/django-pg-current-timestamp

Add true postgresql `CURRENT_TIMESTAMP` support to Django + PostgreSQL.

Also includes automatic support for usage in `auto_now` and `auto_now_add` [DateTimeField](https://docs.djangoproject.com/en/dev/ref/models/fields/#datetimefield) columns in models.


## About

Author: [Jay Taylor](https://twitter.com/jtaylor) / [ThreatStream](https://threatstream.com/)

License: [BSD](/threatstream/django-pg-current-timestamp/blob/master/LICENCE)

Out of the box, (at least as of version 1.7) Django uses python-generated timestamps rather than using `CURRENT_TIMESTAMP` SQL statements.  This plugin module provides the ability to regain this fine-grained control over temporal aspects of the database.


## Installation and Usage

### 1. Install the `django_pg_current_timestamp` package.

#### Automatically via pip + pypi:

    pip install django-pg-current-timestamp

#### Automatically via pip + github:

    pip install -e git+https://github.com/threatstream/django-pg-current-timestamp.git#egg=django-pg-current-timestamp

#### Manually:

    git clone https://github.com/threatstream/django-pg-current-timestamp.git
    cd django-pg-current-timestamp
    python setup.py build
    python setup.py install

### 2. Add `django_pg_current_timestamp` to list of `INSTALLED_APPS` in `settings.py`.

#### settings.py:

    INSTALLED_APPS += ['django_pg_current_timestamp']

### 3. Activate automatic support for DateTimeField `auto_now=True` and `auto_now_add=True` columns by running the package's `init()` method in settings.py.

#### settings.py:

    import django_pg_current_timestamp
    django_pg_current_timestamp.init()


## Manual use of and control over `CURRENT_TIMESTAMP` statements is now achievable

    from django_pg_current_timestamp import CurrentTimestamp

    mm = MyModel.objects.get(id=1)
    mm.last_seen_date = CurrentTimestamp()
    mm.save()
    ## Resulting SQL:
    ##     UPDATE "my_model" SET "last_seen_date" = CURRENT_TIMESTAMP;
 
    print MyModel.objects.filter(last_seen_date__lt=CURRENT_TIME).count()

    MyModel.objects.filter(id__in=[1, 2, 3]).update(last_seen_date=CURRENT_TIME)


## Running the test suite

Grab the source code:

    git clone https://github.com/threatstream/django_pg_current_timestamp.git
    cd django_pg_current_timestamp

Ensure a postgres database named "django_pg_current_timestamp" is available and can be reached from your environment without a password (otherwise it is necessary to edit `DATABASES` in [runtests.py](/threatstream/django-pg-current-timestamp/blob/master/runtests.py)):

    psql -c 'CREATE DATABASE "django_pg_current_timestamp";'

Then simply execute the test runner:

    python runtests.py

