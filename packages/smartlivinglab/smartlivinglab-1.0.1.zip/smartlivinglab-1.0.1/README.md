Smartlivinglab is a small django application designed to store data from sensors.

Is heavily based on Django Rest Framework, as it exposes recolected data via an API. Also includes a write option to store data using the REST API.

INSTALATION
===========

Install using pip
-----------------

pip install smartlivinglab

Add to the INSTALLED_APPS
------------------------

INSTALLED_APPS = (
	       ...
	       rest_framework,
	       rest_framework.authtoken,
	       smartlivinglab,
	       #if you want some simple graphics uncomment this
	       #smartlivinglab.samples
	       ...
	       )

Run database migration
----------------------

$ python manage.py migrate


	       
