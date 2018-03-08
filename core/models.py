from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

class GeneralCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 191
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

    def get_tags(self):
        if hasattr(self, 'tag'):
            return "\n".join([p.name for p in self.tag.all()])

    get_tags.short_description = _('Tags')

    def get_modules(self):
        if hasattr(self, 'module'):
            return "\n".join([p.name for p in self.module.all()])

    get_modules.short_description = _('Modules')

    def get_medicines(self):
        if hasattr(self, 'medicine'):
            return "\n".join([p.name for p in self.medicine.all()])

    get_medicines.short_description = _('Medicine')



class Position(TimeStampedModel):
    name = GeneralCharField(unique=True)
    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

class Banner(TimeStampedModel):
    name = GeneralCharField()
    link = GeneralCharField(blank=True, null=True)
    image = models.ImageField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')


class Module(TimeStampedModel):
    name = GeneralCharField(unique=True)
    desc = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')

class Category(TimeStampedModel):
    name = GeneralCharField()
    slug = models.SlugField(max_length=191)
    desc = models.TextField(blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    module = models.ManyToManyField(Module)
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Tag(TimeStampedModel):
    name = GeneralCharField()
    slug = models.SlugField(max_length=191, blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Post(TimeStampedModel):
    name = GeneralCharField()
    desc = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=191, blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    module = models.ManyToManyField(Module)
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

class Medicine(TimeStampedModel):
    name = GeneralCharField()
    desc = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=191, blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    module = models.ManyToManyField(Module)
    class Meta:
        verbose_name = _('Medicine')
        verbose_name_plural = _('Medicines')

class Disease(TimeStampedModel):
    name = GeneralCharField()
    desc = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=191, blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    module = models.ManyToManyField(Module)
    medicine = models.ManyToManyField(Medicine)
    class Meta:
        verbose_name = _('Disease')
        verbose_name_plural = _('Diseases')

class Expert(TimeStampedModel):
    name = GeneralCharField()
    desc = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=191, blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    module = models.ManyToManyField(Module)
    medicine = models.ManyToManyField(Medicine)
    class Meta:
        verbose_name = _('Expert')
        verbose_name_plural = _('Experts')        

class Drug(TimeStampedModel):
    name = GeneralCharField()
    desc = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=191, blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    #content = models.TextField(blank=True, null=True)
    
    thanhphan = models.TextField(blank=True, null=True)
    dangbaoche = models.TextField(blank=True, null=True)
    chidinh = models.TextField(blank=True, null=True)
    lieudung = models.TextField(blank=True, null=True)
    
    views = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    module = models.ManyToManyField(Module)
    medicine = models.ManyToManyField(Medicine)
    class Meta:
        verbose_name = _('Drug')
        verbose_name_plural = _('Drugs')

