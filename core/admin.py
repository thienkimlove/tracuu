from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _


# Register your models here.
from django.template.response import TemplateResponse
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export.formats import base_formats
from jsoneditor.forms import JSONEditor

from core.forms import *
from core.entry import LogEntryAdmin
from core.models import *
from core.resources import *
from core.filters import *


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class GeneralWithTagAdmin(admin.ModelAdmin):

    search_fields = ['name', ]
    list_filter = (
       'category',
       'status',
    )

    def get_queryset(self, request):
        return super(GeneralWithTagAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'template', 'parent', 'created_at', 'status')
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)


class PostAdmin(ExportMixin, GeneralWithTagAdmin):
    list_display = ('name', 'category', 'image_tag', 'views', 'tag_list', 'created_at', 'status')

    form = PostForm
    autocomplete_fields = ['category']
    resource_class = PostResource
    to_encoding = "utf8mb4"
    formats = [
        base_formats.XLS,
    ]

admin.site.register(Post, PostAdmin)


class ExpertAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'link', 'created_at', 'status')


admin.site.register(Expert, ExpertAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'channel', 'turns', 'created_at', 'status')
    search_fields = ['name']

admin.site.register(Video, VideoAdmin)

admin.site.register(LogEntry, LogEntryAdmin)
