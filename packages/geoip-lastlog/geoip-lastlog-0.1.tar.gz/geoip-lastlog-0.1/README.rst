
geoip-lastlog
=============

Geolocation for motd / ssh last login based on lastlog

.. image:: https://pypip.in/download/geoip-lastlog/badge.png
    :target: https://pypi.python.org/pypi/geoip-lastlog/
    :alt: Downloads

.. image:: https://pypip.in/version/geoip-lastlog/badge.png
    :target: https://pypi.python.org/pypi/geoip-lastlog/
    :alt: Latest Version

.. image:: https://pypip.in/license/geoip-lastlog/badge.png
    :target: https://pypi.python.org/pypi/geoip-lastlog/
    :alt: License


Installation
------------

On Debian and its derivatives, install the dependencies:

   $ apt-get install python-arrow python-geoip geoip-database-contrib

geoip-database-contrib provides geolocation at city level. In alternative, you can install geoip-database which provides only the country names:

   $ apt-get install python-arrow python-geoip geoip-database

Then, install geoip-lastlog from GitHub or from PyPI:

   $ git clone git://github.com/FedericoCeratto/geoip-lastlog

or, create a virtualenv and then fetch it from PyPI:

   $ pip install geoip-lastlog


Usage
-----

Add the script to the end of your /etc/profile

   /<fullpath>/geoip_lastlog.py

Optionally, you can specify how many entries to print:

   /<fullpath>/geoip_lastlog.py <N>


