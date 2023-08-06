Cmsplugin tab ui
==================

Tab plugin for django cms with Jquery UI

Compatible with django 1.7 and django cms 3.0.6

.. note:: It has problems with admin toolbar, tab effect  not found because django cms put extra div in admin view. 

Installation 
==============

Install from pypi 

.. code:: bash

	$ pip install cmsplugin_tab_ui
	
And put in your ``settings`` apps 

.. code:: python

    INSTALLED_APPS = (
        ...
        'cmsplugin_tab_ui',
        'paintstore',
    )

Run syncdb or migrate if you use django 1.7

.. code:: python 

    $ python manage.py syncdb
    $ python manager.py migrate
    



