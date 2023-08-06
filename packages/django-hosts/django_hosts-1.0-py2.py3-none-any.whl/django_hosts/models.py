import django
from django.conf import settings
from django.template import add_to_builtins

from .cache import patch_cache_key_funcs

if django.VERSION[:2] < (1, 7):
    if getattr(settings, 'HOST_OVERRIDE_URL_TAG', False):  # pragma: no cover
        add_to_builtins('django_hosts.templatetags.hosts_override')

    patch_cache_key_funcs()
