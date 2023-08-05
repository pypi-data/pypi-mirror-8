cmsplugin-tab-ui
================

Tab plugin for django cms with Jquery UI

Installation 
==============

Install from pypi 

	$ pip install cmsplugin_tab_ui
	
And put in your ``settings`` apps 

    INSTALLED_APPS = (
        ...
        'cmsplugin_tab_ui',
    )

Run syncdb or migrate if you use django 1.7

    $ python manage.py syncdb
    $ python manager.py migrate
    

Use
===== 

In your base template include jquery 

	 <script src="//code.jquery.com/jquery-1.10.2.js"></script>


