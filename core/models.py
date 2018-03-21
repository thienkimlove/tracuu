from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core.widgets import EditorTextArea


class GeneralCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 191
        super().__init__(*args, **kwargs)

def vi_slug(data):
    vietnamese_map = {
        ord(u'o'): 'o', ord(u'ò'): 'o', ord(u'ó'): 'o', ord(u'ỏ'): 'o', ord(u'õ'): 'o', ord(u'ọ'): 'o',
        ord(u'ơ'): 'o', ord(u'ờ'): 'o', ord(u'ớ'): 'o', ord(u'ở'): 'o', ord(u'ỡ'): 'o', ord(u'ợ'): 'o',
        ord(u'ô'): 'o', ord(u'ồ'): 'o', ord(u'ố'): 'o', ord(u'ổ'): 'o', ord(u'ỗ'): 'o', ord(u'ộ'): 'o',

        ord(u'à'): 'a', ord(u'á'): 'a', ord(u'á'): 'a', ord(u'ả'): 'a', ord(u'ã'): 'a', ord(u'ạ'): 'a',
        ord(u'ă'): 'a', ord(u'ắ'): 'a', ord(u'ằ'): 'a', ord(u'ẳ'): 'a', ord(u'ẵ'): 'a', ord(u'ạ'): 'a',
        ord(u'â'): 'a', ord(u'ầ'): 'a', ord(u'ấ'): 'a', ord(u'ậ'): 'a', ord(u'ẫ'): 'a', ord(u'ẩ'): 'a',

        ord(u'đ'): 'd', ord(u'Đ'): 'd',

        ord(u'è'): 'e', ord(u'é'): 'e', ord(u'ẻ'): 'e', ord(u'ẽ'): 'e', ord(u'ẹ'): 'e',
        ord(u'ê'): 'e', ord(u'ề'): 'e', ord(u'ế'): 'e', ord(u'ể'): 'e', ord(u'ễ'): 'e', ord(u'ệ'): 'e',

        ord(u'ì'): 'i', ord(u'í'): 'i', ord(u'ỉ'): 'i', ord(u'ĩ'): 'i', ord(u'ị'): 'i',
        ord(u'ư'): 'u', ord(u'ừ'): 'u', ord(u'ứ'): 'u', ord(u'ử'): 'ữ', ord(u'ữ'): 'u', ord(u'ự'): 'u',
        ord(u'ý'): 'y', ord(u'ỳ'): 'y', ord(u'ỷ'): 'y', ord(u'ỹ'): 'y', ord(u'ỵ'): 'y',
    }
    data = (data[:200]) if len(data) > 200 else data
    slug = slugify(data.translate(vietnamese_map))
    return slug

class GeneralTextField(models.TextField):
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

class SiteSlug(models.Model):
    slug = GeneralCharField(unique=True)

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

    def _get_unique_slug(self):
        if hasattr(self, 'slug') and hasattr(self, 'name'):
            slug = vi_slug(self.name)
            unique_slug = slug
            num = 1
            while SiteSlug.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
            SiteSlug.objects.create(slug=unique_slug)
            return unique_slug

    def save(self, *args, **kwargs):
        if hasattr(self, 'slug'):
            if not self.slug:
                self.slug = self._get_unique_slug()
        super().save()


    def __str__(self):
        if hasattr(self, 'name'):
            return "{0}".format(self.name)

    def get_absolute_url(self):
        if hasattr(self, 'slug'):
            return '/%s.html' % self.slug
        return ''

    def image_tag(self):
        if hasattr(self, 'image') and self.image:
            return mark_safe('<img src="%s" width="150" />' % self.image.url)
        return None
    image_tag.short_description = _('Image')

    def get_science_name(self):
        if hasattr(self, 's_name'):
            return "{0}".format(self.s_name)

    get_science_name.short_description = _('Tên khoa học')



class Category(TimeStampedModel):

    TEMPLATE_CHOICES = (
        ('post', _("Loại tin tức")),
        ('medicine', _("Loại tra cứu dược liệu")),
        ('special', _("Loại tra cứu danh lục")),
        ('drug', _("Loại tra cứu bài thuốc")),
        ('disease', _("Loại tra cứu bệnh"))
    )

    name = GeneralCharField()
    slug = GeneralSlug()
    desc = models.TextField(blank=True, null=True)
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    status = models.BooleanField(default=True)
    banner_image = models.ImageField(blank=True, null=True)
    template = GeneralCharField(choices=TEMPLATE_CHOICES, default='post')
    display_order=models.PositiveSmallIntegerField(default=0)
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        if hasattr(self, 'slug'):
            return '/%s' % self.slug
        return ''

class Post(TimeStampedModel):
    name = GeneralCharField()

    s_name = GeneralCharField(blank=True, null=True)
    vi_name = GeneralCharField(blank=True, null=True)
    other_name = GeneralCharField(blank=True, null=True)
    last_name = GeneralCharField(blank=True, null=True)

    desc = models.TextField(blank=True, null=True)
    slug = GeneralSlug()
    seo_name = GeneralCharField(blank=True, null=True)
    seo_desc = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)

    galery_image1 = models.ImageField(blank=True, null=True)
    galery_image2 = models.ImageField(blank=True, null=True)
    galery_image3 = models.ImageField(blank=True, null=True)


    content = models.TextField(blank=True, null=True)
    thanhphan = models.TextField(blank=True, null=True)
    dangbaoche = models.TextField(blank=True, null=True)
    chidinh = models.TextField(blank=True, null=True)
    lieudung = models.TextField(blank=True, null=True)


    views = models.IntegerField(default=0, editable=False)
    tags = TaggableManager()
    disease = models.ManyToManyField("self", related_name='child_disease')

    class Meta:
        verbose_name = _('Bài viết')
        verbose_name_plural = _('Bài viết')


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