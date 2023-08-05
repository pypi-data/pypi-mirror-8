# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from .shortcuts import get_usersettings_model

USERSETTINGS_CACHE = {}


class UserSettingsManager(models.Manager):

    def get_current(self):
        """
        Returns the current ``UserSettings`` based on the SITE_ID in the
        project's settings. The ``UserSettings`` object is cached the first
        time it's retrieved from the database.
        """
        from django.conf import settings
        try:
            site_id = settings.SITE_ID
        except AttributeError:
            raise ImproperlyConfigured(
                'You\'re using the Django "sites framework" without having '
                'set the SITE_ID setting. Create a site in your database and '
                'set the SITE_ID setting to fix this error.')

        try:
            current_usersettings = USERSETTINGS_CACHE[site_id]
        except KeyError:
            current_usersettings = self.get(site_id=site_id)
            USERSETTINGS_CACHE[site_id] = current_usersettings
        return current_usersettings

    def clear_cache(self):
        """Clears the ``UserSettings`` object cache."""
        global USERSETTINGS_CACHE
        USERSETTINGS_CACHE = {}


class UserSettings(models.Model):
    site = models.OneToOneField(
        Site, editable=False, null=True, related_name='usersettings')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, related_name='usersettings')
    created = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified = models.DateTimeField(_('Last Updated'), auto_now=True)

    objects = UserSettingsManager()

    class Meta:
        verbose_name = _('User Setting')
        verbose_name_plural = _('User Settings')
        abstract = True

    def __str__(self):
        return force_text(self.site)


def clear_usersettings_cache(sender, **kwargs):
    """
    Clears the cache (if primed) each time a ``UserSettings`` is saved or deleted
    """
    instance = kwargs['instance']
    try:
        del USERSETTINGS_CACHE[instance.site.pk]
    except KeyError:
        pass


import django
from distutils.version import LooseVersion

if LooseVersion(django.get_version()) < LooseVersion('1.7'):
    pre_save.connect(clear_usersettings_cache, sender=get_usersettings_model())
    pre_delete.connect(clear_usersettings_cache, sender=get_usersettings_model())
