wsgiappversion
==============

What does it do?
----------------

Adds a ``/version`` url that returns a json response of the current
application version.

Example usage:

  .. code-block:: python

      from wsgiappversion import ApplicationVersion
      from my_project import MyWSGIApp

      application = MyWSGIApp()
      application = ApplicationVersion(application, determine_version='my_project')

The required ``determine_version`` argument is used to determine what the
current version actually is. ``determine_version`` can be either a string or a
callable that takes no arguments. When a string is used then the version is
determined by calling ``pkg_resources.require(package_name)``. If that would
not work for your application then a callable that returns the correct
version can be used.

Since a package version would likely not change without an application
restart we would recommend using a closure (or some other similar method of
caching a value) as your callable.
