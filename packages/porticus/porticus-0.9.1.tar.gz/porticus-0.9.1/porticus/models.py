"""
Models for porticus
"""
import os

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from porticus.managers import RessourcePublishedManager, GalleryPublishedManager, AlbumPublishedManager

from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

from tagging.fields import TagField
from tagging.models import Tag

PUBLISHED_CHOICES = (
    (True, _('Published')),
    (False, _('Unpublished')),
)

class Gallery(models.Model):
    """Model representing a gallery"""

    name = models.CharField(_('name'), max_length=250)

    description = models.TextField(_('description'), blank=True)

    image = FilerImageField(verbose_name=_('image'), related_name="gallery_image", null=True, blank=True, default=None)

    template_name = models.CharField(_('template'), max_length=255, help_text=_('Template used to render the gallery'), choices=settings.PORTICUS_GALLERY_TEMPLATE_CHOICES, default=settings.PORTICUS_GALLERY_TEMPLATE_DEFAULT)

    publish = models.BooleanField(_('published'), choices=PUBLISHED_CHOICES, default=True)

    priority = models.IntegerField(_('display priority'), default=100)

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    slug = models.SlugField(_('slug'), unique=True, max_length=100)

    objects = models.Manager()
    published = GalleryPublishedManager()

    #@models.permalink
    #def get_absolute_url(self):
        #return ('porticus-gallery-detail', (self.slug,))

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('-priority', 'name')
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')


class Album(MPTTModel):
    """Model representing an album"""
    gallery = models.ForeignKey(Gallery)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    name = models.CharField(_('name'), max_length=250)

    description = models.TextField(_('description'), blank=True)

    image = FilerImageField(verbose_name=_('image'), related_name="album_image", null=True, blank=True, default=None)

    template_name = models.CharField(_('template'), max_length=255, help_text=_('Template used to render the album'), choices=settings.PORTICUS_ALBUM_TEMPLATE_CHOICES, default=settings.PORTICUS_ALBUM_TEMPLATE_DEFAULT)

    publish = models.BooleanField(_('published'), choices=PUBLISHED_CHOICES, default=True)
    
    priority = models.IntegerField(_('display priority'), default=100)

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    slug = models.SlugField(_('slug'), unique=True, max_length=100)

    def __unicode__(self):
        return self.name

    objects = TreeManager()
    published = AlbumPublishedManager()

    #@models.permalink
    #def get_absolute_url(self):
        #return ('porticus-album-detail', (self.gallery.slug, self.slug,))

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_published_children(self):
        """
        Return all ressources for the album and all its children
        """
        return self.get_children().filter(publish=True)
    
    def get_published_descendants(self):
        """
        Return all ressources for the album and its direct descendants
        """
        return self.get_descendants().filter(publish=True)
    
    def get_published_ressources(self):
        """
        Return all ressources for the album
        """
        return self.ressource_set.filter(publish=True).order_by('priority', 'name')

    class Meta:
        verbose_name = _('album')
        verbose_name_plural = _('albums')

    class MPTTMeta:
        order_insertion_by = ['gallery', 'priority', 'name']


class Ressource(models.Model):
    """Model for representing a ressource"""
    album = models.ForeignKey(Album)

    name = models.CharField(_('name'), max_length=250)

    description = models.TextField(_('description'), blank=True)

    image = FilerImageField(verbose_name=_('image'), related_name="ressource_image", null=True, blank=True, default=None)

    file_type = models.IntegerField(_('file type'), choices=settings.PORTICUS_RESSOURCE_FILETYPE_CHOICES, default=settings.PORTICUS_RESSOURCE_FILETYPE_DEFAULT)
    file = FilerFileField(verbose_name=_('file'), related_name="ressource_file", null=True, blank=True, default=None)
    file_url = models.URLField(_('file url'), blank=True)
    file_weight = models.CharField(_('file weight'), blank=True, max_length=15)

    publish = models.BooleanField(_('published'), choices=PUBLISHED_CHOICES, default=True)

    priority = models.IntegerField(_('display priority'), default=100)

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    tags = TagField(_('tags'))

    objects = models.Manager()
    published = RessourcePublishedManager()

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    @property
    def get_file(self):
        try:
            return self.file_url or self.file.url
        except ValueError:
            return None


    def clean(self):
        if not self.get_file:
            raise ValidationError(_('Please upload a file or give a file url'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('-priority', 'name')
        verbose_name = _('ressource')
        verbose_name_plural = _('ressources')
