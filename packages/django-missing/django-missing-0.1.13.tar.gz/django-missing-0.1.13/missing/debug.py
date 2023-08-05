import re

from django.views import debug

debug.HIDDEN_SETTINGS = re.compile(debug.HIDDEN_SETTINGS.pattern + '|URL|CSRF|COOKIE|csrftoken|sessionid')

class SafeExceptionReporterFilter(debug.SafeExceptionReporterFilter):
    """
    Safe exception reporter filter which also filters request environment
    (``META``) and cookies (``COOKIES``) so that it is safer to share the
    report publicly.

    This is useful to not display passwords and other sensitive data passed to
    Django through its process environment.

    Furthermore, it configures Django to additionally clean settings with
    ``URL``, ``CSRF``, ``COOKIE``, ``csrftoken``, and ``sessionid`` in keys.

    To install it, configure Django to::

        DEFAULT_EXCEPTION_REPORTER_FILTER = 'missing.debug.SafeExceptionReporterFilter'

    and import ``missing.debug`` somewhere in your code, for example, in ``urls.py``
    of your project.

    .. note:: Requires Django 1.4+.
    """

    def get_post_parameters(self, request):
        # We hook into this method to modify request in place, not nice, but it works
        for key in request.META:
            if key.isupper():
                request.META[key] = debug.cleanse_setting(key, request.META[key])
        for key in request.COOKIES:
            request.COOKIES[key] = debug.cleanse_setting(key, request.COOKIES[key])

        return super(SafeExceptionReporterFilter, self).get_post_parameters(request)
