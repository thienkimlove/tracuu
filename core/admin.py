from django.conf.urls import url
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# Register your models here.
from django.template.response import TemplateResponse
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export.formats import base_formats
from jsoneditor.forms import JSONEditor

from core.forms import *
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


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', )
    search_fields = ["name"]
    ordering = ["-created_at"]

admin.site.register(Position, PositionAdmin)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'image_tag', 'position', 'created_at', 'status')
    readonly_fields = ('image_tag',)

    list_filter = (
        ('position__name', custom_titled_filter('position name')),
        'link',
    )
    search_fields = ["link"]
    ordering = ["-created_at"]
    fieldsets = (
        (None, {
            'fields': ('name', 'link', 'position', 'image')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )


admin.site.register(Banner, BannerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_modules', 'parent', 'created_at', 'status')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'seo_name', 'seo_desc', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

admin.site.register(Tag, TagAdmin)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'created_at')
    search_fields = ['name']

admin.site.register(Module, ModuleAdmin)

class PostAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'category', 'image_tag', 'views', 'get_modules', 'get_tags', 'created_at', 'status')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('views',)
    search_fields = ['name']
    list_filter = (
        'category',
        'status',
    )
    form = PostForm
    autocomplete_fields = ['category', 'tag', 'module']
    resource_class = PostResource
    to_encoding = "utf8mb4"
    formats = [
        base_formats.XLS,
    ]

admin.site.register(Post, PostAdmin)

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'views', 'get_modules', 'get_tags', 'created_at', 'status')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('views',)
    search_fields = ['name']
    list_filter = (
        'status',
    )
    form = MedicineForm
    autocomplete_fields = ['tag', 'module']


admin.site.register(Medicine, MedicineAdmin)

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'views', 'get_modules', 'get_tags', 'created_at', 'status')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('views',)
    search_fields = ['name']
    list_filter = (
        'status',
    )
    form = DiseaseForm
    autocomplete_fields = ['tag', 'module']


admin.site.register(Disease, DiseaseAdmin)

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'views', 'get_modules', 'get_tags', 'created_at', 'status')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('views',)
    search_fields = ['name']
    list_filter = (
        'status',
    )
    form = DrugForm
    autocomplete_fields = ['tag', 'module']


admin.site.register(Drug, DrugAdmin)

class ExpertAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'views', 'get_modules', 'get_tags', 'created_at', 'status')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('views',)
    search_fields = ['name']
    list_filter = (
        'status',
    )
    form = ExpertForm
    autocomplete_fields = ['tag', 'module']


admin.site.register(Expert, ExpertAdmin)
