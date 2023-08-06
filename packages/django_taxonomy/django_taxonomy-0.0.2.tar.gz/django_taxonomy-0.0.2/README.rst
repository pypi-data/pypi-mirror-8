===================
Django taxonomy
===================

Base class which provides convenient categorising methods to use as a foreign key to models

Quickstart
==========

Add apps to installed apps
--------------------------

Add

    'taxonomy',
    'mptt',

to your INSTALLED_APPS.

Prepare Database
----------------

    ./manage.py migrate

Usage
=====

Simply extend TaxonomyModel when creating your categories. The model has the attributes name, slug, parent, weight and published
