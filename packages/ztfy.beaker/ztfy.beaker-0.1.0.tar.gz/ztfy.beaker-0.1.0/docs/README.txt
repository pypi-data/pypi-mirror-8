.. contents::

Introduction
============

ZTFY.beaker is a small wrapper around Beaker (http://pypi.python.org/pypi/Beaker)
session and caching library.

It allows you to define a Beaker session throught a ZCML configuration directive to include it
in a WSGI application based on ZTFY packages.

A BeakerSessionUtility can then be created and registered to act as a session data container.


Beaker session configurations
=============================

All Beaker session options can be defined throught ZCML directives. See `metadirectives.py` to get
the complete list of configuration options.

For example, to define a Memcached session configuration::

	<configure
		xmlns:beaker="http://namespaces.ztfy.org/beaker">

		<beaker:memcachedSession
			url="127.0.0.1:11211"
			cookie_expires="False"
			lock_dir="/var/lock/sessions" />

	</configure>


Directives are available for memory, DBM, file, Memcached and SQLAlchemy sessions storages.
