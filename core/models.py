from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django import forms

from core.widgets import EditorTextArea


class GeneralCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 191
        super().__init__(*args, **kwargs)



class GeneralTextField(models.TextField):

    def to_python(self, value):
        """Return a text."""
        if value in self.empty_values:
            return self.empty_value
        return value

    def formfield(self, **kwargs):
        # Passing max_length to forms.CharField means that the value's length
        # will be validated twice. This is considered acceptable since we want
        # the value in the form field (to pass into widget for example).
        defaults = {'max_length': self.max_length}
        if not self.choices:
            defaults['widget'] = EditorTextArea
        defaults.update(kwargs)
        return super().formfield(**defaults)

class GeneralSlug(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 191
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['editable'] = False
        kwargs['db_index'] = True
        super().__init__(*args, **kwargs)

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ["-created_at"]


    def __str__(self):
        if hasattr(self, 'name'):
            return "{0}".format(self.name)

    def get_absolute_url(self):
        pass

    def image_tag(self):
        if hasattr(self, 'image') and self.image:
            return mark_safe('<img src="%s" width="150" />' % self.image.url)
        return None
    image_tag.short_description = _('Image')

    def get_science_name(self):
        if hasattr(self, 's_name'):
            return "{0}".format(self.s_name)

    get_science_name.short_description = _('Tên khoa học')

    def save(self, *args, **kwargs):
        if hasattr(self, 'name') and hasattr(self, 'slug'):
            self.slug = slugify(self.name)
        super(TimeStampedModel, self).save(*args, **kwargs)


class Category(TimeStampedModel):
    name = GeneralCharField()
    slug = GeneralSlug()
    desc = models.TextField(blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Post(TimeStampedModel):
    name = GeneralCharField()
    desc = models.TextField(blank=True, null=True)
    slug = GeneralSlug()
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0, editable=False)
    tags = TaggableManager()
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

class Disease(TimeStampedModel):
    name = GeneralCharField()
    s_name = GeneralCharField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    slug = GeneralSlug()
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0, editable=False)
    tags = TaggableManager()
    class Meta:
        verbose_name = _('Disease')
        verbose_name_plural = _('Diseases')

class Medicine(TimeStampedModel):
    name = GeneralCharField()
    s_name = GeneralCharField(blank=True, null=True)
    other_name = GeneralCharField(blank=True, null=True)
    last_name = GeneralCharField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    slug = GeneralSlug()
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    galery_image1 = models.ImageField(blank=True, null=True)
    galery_image2 = models.ImageField(blank=True, null=True)
    galery_image3 = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0, editable=False)
    tags = TaggableManager()
    disease = models.ManyToManyField(Disease, blank=True)
    class Meta:
        verbose_name = _('Medicine')
        verbose_name_plural = _('Medicines')

class Special(TimeStampedModel):
    name = GeneralCharField()
    s_name = GeneralCharField(blank=True, null=True)
    other_name = GeneralCharField(blank=True, null=True)
    last_name = GeneralCharField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    slug = GeneralSlug()
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    galery_image1 = models.ImageField(blank=True, null=True)
    galery_image2 = models.ImageField(blank=True, null=True)
    galery_image3 = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0, editable=False)
    tags = TaggableManager()
    disease = models.ManyToManyField(Disease, blank=True)
    class Meta:
        db_table = 'core_special'
        verbose_name = _('Danh lục')
        verbose_name_plural = _('Danh lục')


class Drug(TimeStampedModel):
    name = GeneralCharField()
    s_name = GeneralCharField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    slug = GeneralSlug()
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    thanhphan = models.TextField(blank=True, null=True)
    dangbaoche = models.TextField(blank=True, null=True)
    chidinh = models.TextField(blank=True, null=True)
    lieudung = models.TextField(blank=True, null=True)
    
    views = models.IntegerField(default=0, editable=False)
    tags = TaggableManager()
    class Meta:
        verbose_name = _('Drug')
        verbose_name_plural = _('Drugs')

class Expert(TimeStampedModel):
    name = GeneralCharField()
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    link = GeneralCharField(blank=True, null=True)
    class Meta:
        verbose_name = _('Expert')
        verbose_name_plural = _('Experts')


class Video(TimeStampedModel):
    name = GeneralCharField(blank=True, null=True)
    link = GeneralCharField(blank=True, null=True)
    channel = GeneralCharField(blank=True, null=True)
    turns = GeneralCharField(blank=True, null=True)
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')