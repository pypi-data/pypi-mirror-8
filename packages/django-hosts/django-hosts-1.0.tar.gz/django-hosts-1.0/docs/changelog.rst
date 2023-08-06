Changelog
=========

1.0 (2014-12-29)
----------------

- Moved repo to https://github.com/jezdez/django-hosts

- Extended testing setup to Python 3.4 and Django 1.7.

- Dropped support for Django 1.5 as it doesn't receive any security releases
  anymore and 1.4 since it's very soon going to lose it's LTS status.

- Optionally allow setting the port per host and using the
  :attr:`~django.conf.settings.HOST_PORT` setting.

- Moved ``django_hosts.reverse.reverse_full`` to
  :func:`django_hosts.resolvers.reverse` and
  ``django_hosts.reverse.reverse_host`` to
  :func:`django_hosts.resolvers.reverse_host`. This is a cleanup process to
  easier map Django's features and normalize the call signatures. The old
  functions are now pending deprecation and will be removed in the 1.2 release.

- Refactored :func:`~django_hosts.templatetags.hosts.host_url` template tag
  to closer follow Django's own url template tag. This includes:

  - the renaming of the ``on`` argument to ``host`` (``on`` will be removed
    in the 1.2 release)
  - the use of the Django>1.5 url template tag syntax that requires the view
    name (and the host name) to be quoted unless it's meant to be a template
    context variable

    Old::

      {% host_url homepage on www %}

    New::

      {% host_url 'homepage' host 'www' %}

  - the ability to automatically fallback to the host as defined
    in the :attr:`~django.conf.settings.DEFAULT_HOST` setting when no
    ``host`` name is passed
  - a new optional ``scheme`` parameter to override the resulting URL's scheme
    individually
  - a new optional ``port`` parameter to override the resulting URL's port
    individually
  - a new ability to override Django's built-in url template tag by setting
    the :attr:`~django.conf.setting.HOST_OVERRIDE_URL_TAG` setting to ``True``

- Added :func:`~django_hosts.resolvers.reverse_lazy` and
  :func:`~django_hosts.resolvers.reverse_host_lazy` for use in import time
  situations such as class based views.

- Split the :class:`django_hosts.middleware.HostsMiddleware` middleware into
  two piece to enable the use of the ``request.host`` parameter in other
  middlewares. See the installation instruction for the new setup.

- Rely on a few more built-ins in Django instead of writing them ourselves.

- Moved the test suite to use the py.test runner instead of Django's own test
  runner.

- Updated the :doc:`faq` to explain how to use Django's full page caching
  middleware with Django<1.7 and fixed the entry about the compatibility to
  the Debug Toolbar.

- Extended the tests to be close to 100% test coverage.

- Added tox configuration for easy local tests.

- Added a few Django 1.7 system checks (for the ``ROOT_HOSTCONF`` and
  ``DEFAULT_HOST`` settings).

0.6 (2013-06-17)
----------------

- Support for Django 1.5.x and Python > 3.2.

- Dropped support for Python 2.5 and Django 1.3.

- Optionally allow setting the scheme per host instead of only using
  the :attr:`~django.conf.settings.HOST_SCHEME` setting.

0.5 (2012-08-29)
----------------

- Fixed host reversing when the ``PARENT_HOST`` equals

- Added :attr:`~django.conf.settings.HOST_SCHEME` setting to be able to
  override the default URL scheme when reversing hosts.

0.4.2 (2012-02-14)
------------------

- Removed a unneeded installation time requirement for Django <= 1.4.

- Removed the use of versiontools due to unwanted installation time side
  effects.

- Refactored tests slightly.

0.4.1 (2011-12-23)
------------------

- Added :func:`~django_hosts.callbacks.cached_host_site` callback which
  stores the matching :class:`~django.contrib.sites.models.Site` instance
  in the default cache backend (also see new
  :attr:`~django.conf.settings.HOST_SITE_TIMEOUT` setting).

- Throw warning if django-debug-toolbar is used together with the
  ``django_hosts`` and the order of the ``MIDDLEWARE_CLASSES`` setting
  isn't correct.

- Added CI server at https://ci.enn.io/job/django-hosts/

0.4 (2011-11-04)
----------------

- Added ability to :ref:`save the result<asvar>` of
  :func:`~django_hosts.templatetags.hosts.host_url` template tag in a
  template context variable.

0.3 (2011-09-30)
----------------

- Consolidated reversal internals.

- Removed unfinished support for the Django Debug Toolbar.

- Added a custom callback which uses Django's sites_ app to retrieve
  a ``Site`` instance matching the current host, setting ``request.site``.

- Extended tests dramatically (100% coverage).

- Added docs at http://django-hosts.rtfd.org

- Stopped preventing the name 'default' for hosts.

.. _sites: https://docs.djangoproject.com/en/dev/ref/contrib/sites/

0.2.1 (2011-05-31)
------------------

- Fixed issue related to the ``PARENT_HOST`` setting when used with
  empty host patterns.

- Stopped automatically emulating hosts in debug mode.

0.2 (2011-05-31)
----------------

- **BACKWARDS INCOMPATIBLE** Renamed the package to ``django_hosts``

  Please change your import from::

    from hosts import patterns, hosts

  to::

    from django_hosts import patterns, hosts

- **BACKWARDS INCOMPATIBLE** Changed the data type that the
  ``django_hosts.patterns`` function returns to be a list instead of a
  SortedDict to follow conventions of Django's URL patterns.
  You can use that for easy extension of the patterns, e.g.::

    from django_hosts import patterns, host
    from mytemplateproject.hosts import host_patterns

    host_patterns += patterns('',
        host('www2', 'mysite.urls.www2', name='www2')
    )

- Extended tests to have full coverage.

- Fixed prefix handling.

0.1.1 (2011-05-30)
------------------

- Fixed docs issues.

- Use absolute imports where possible.

0.1 (2011-05-29)
----------------

- Initial release with middleware, reverse and templatetags.
