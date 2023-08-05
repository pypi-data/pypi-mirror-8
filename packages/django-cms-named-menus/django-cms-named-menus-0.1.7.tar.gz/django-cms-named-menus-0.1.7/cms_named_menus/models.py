from django.db import models
from autoslug.fields import AutoSlugField
from jsonfield import JSONField
import collections


class CMSNamedMenu(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(always_update=True, populate_from='name')
    pages = JSONField(blank=True, null=True,
                      load_kwargs={
                          'object_pairs_hook': collections.OrderedDict
                      },
                      default=[])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "CMS Named Menu"
        verbose_name_plural = "CMS Named Menus"
