from __future__ import unicode_literals
from django.conf import settings as django_settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Setting(models.Model):
    """
    Stores values for ``mezzanine.conf`` that can be edited via the admin.
    """

    prefix = models.CharField(max_length=50)
    name = models.CharField(max_length=150, unique=True)
    value = models.CharField(max_length=2000)
    site = models.ForeignKey("sites.Site", editable=False,
                             related_name='project_setting',
                             default=django_settings.SITE_ID)

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def __str__(self):
        return "%s: %s" % (self.name, self.value)

    def save(self, update_site=False, *args, **kwargs):
        """
        Set the site to the current site when the record is first
        created, or the ``update_site`` argument is explicitly set
        to ``True``.
        """
        if update_site or not self.id:
            self.site_id = django_settings.SITE_ID
        super(Setting, self).save(*args, **kwargs)
        from .conf import settings
        settings._loaded = False
        settings._editable_cache[self.name] = self.value

